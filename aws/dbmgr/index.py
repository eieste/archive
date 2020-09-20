import cfnresponse
from datetime import date, timedelta
import os, json
import pymysql
import boto3
import botocore
import random
import string
import logging

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger("create_database_credentials")


class Secret:

    def __init__(self, source, target):
        self.source = source
        self.target = target

    @staticmethod
    def getSecret(secret_arn):
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=session.region_name
        )

        try:
            logging.info("Try to load secret from SecretsManager for Arn: {}".format(secret_arn))
            get_secret_value_response = client.get_secret_value(SecretId=secret_arn)
        except Exception as e:
            logging.exception(e)
            raise e
        else:
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
                return json.loads(secret)
            raise ValueError("Cant handle Binary secrets")

    @staticmethod
    def updateSecret(secret_arn, altered_secret):
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=session.region_name
        )

        try:
            logging.info("Try to update secret in Arn: {}".format(secret_arn))
            client.update_secret(
                SecretId=secret_arn,
                SecretString=json.dumps(altered_secret)
            )
        except Exception as e:
            logging.error(e)
            raise e


class Helper:

    @staticmethod
    def get_random_string(length, simple=False):
        logging.debug("Create random string with parameters: length={}; simple={}".format(length, simple))
        letters = string.ascii_lowercase

        if not simple:
            letters += string.digits + string.punctation

        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    @staticmethod
    def generateMissingCredential(username, password, database):
        if not username:
            username = "u-{}".format(Helper.get_random_string(8, simple=True))

        if not password:
            password = "p-{}".format(Helper.get_random_string(20))

        if not database:
            database = "d-{}".format(Helper.get_random_string(8, simple=True))
        return username, password, database

def openConnection(host, username, password):
    conn = None
    log.info("Try to open rds Connection")
    if conn is None:
        conn = pymysql.connect(host, user=username, password=password, connect_timeout=5, cursorclass=pymysql.cursors.DictCursor)
    return conn

def handler(event, context, **kwargs):
    logging.debug("Inkomming event: {}".format(json.dumps(event)))
    properties = event["ResourceProperties"]
    secret = Secret(properties.get("SourceSecretArn", False), properties.get("TargetSecretArn", False))

    responseData = {}
    conn = None
    try:
        raw_source_secret = Secret.getSecret(secret.source)
        conn = openConnection(raw_source_secret.get("host"), raw_source_secret.get("username"), raw_source_secret.get("password"))

        if event.get("RequestType") == "Create" or event.get("RequestType") == "Update":
            try:
                create_process(conn, secret)
                cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData)
            except Exception as e:
                logging.exception(e)
                cfnresponse.send(event, context, cfnresponse.FAILED, responseData)
    except Exception as e:
        logging.error(e)
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                logging.exception(e)

    try:
        if event.get("RequestType") == "Delete":
            try:
                cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData)
            except Exception as e:
                logging.exception(e)
                cfnresponse.send(event, context, cfnresponse.FAILED, responseData)
    except Exception as e:
        logging.error(e)


def create_process(conn, secret):
    raw_secret = Secret.getSecret(secret.target)

    username, password, database = Helper.generateMissingCredential(raw_secret.get("username", False), raw_secret.get("password", False), raw_secret.get("database", False))
    with conn.cursor() as cur:

        logging.info("Create new Database")
        cur.execute('CREATE DATABASE IF NOT EXISTS `{}`'.format(database))
        result_set = cur.fetchall()
        log.debug("DB-Create Result: {}".format(result_set))

        logging.info("Create a new User")
        cur.execute('CREATE USER %s@"%%" IDENTIFIED BY %s', (username, password))
        result_set = cur.fetchall()
        log.debug("User-Create Result: {}".format(result_set))

        logging.info("Grant Permission")
        cur.execute('GRANT ALL PRIVILEGES ON `{}`.* TO %s@"%%"'.format(database), username)
        result_set = cur.fetchall()
        log.debug("Grand User Result: {}".format(result_set))

        logging.debug("Database Name: {}".format(database))
        logging.debug("User Name: {}".format(username))

    raw_secret.update({
        "username": username,
        "password": password,
        "database": database
    })

    Secret.updateSecret(secret.target, raw_secret)
