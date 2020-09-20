# dbmgr


 The stack.yaml shows excerpts from a larger stack, so it is probably not 100% valid

The whole construct works as follows:

Cloudformation creates a Lambda function with the content of index.py and dcfnresponse.py

This Lambda function can then be called using a Cloudformation::CustomResource.


As "passing parameter" the Lambda function receives a SourceSecret and a TargetSecret

The SourceSecret contains the admin access to the RDS
The TargetSecret contains the credentials for a "sub account

The lambda function always creates a database to which the new user has access.


if the secrets credentials are missing, random values are generated
