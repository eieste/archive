import os


class Settings:
    """
        Application Settings
    """
    # FlatAPI endpoint Configuration
    # FlatAPI Provides all configuration and meta Information
    FLAT_API_PORT = ":8000"
    FLAT_API_HOST = "192.168.69.1"

    # Memcached Host endpoint; used to cache config if flatapi is not available
    MEMCACHED_HOST = ["127.0.0.1:11211"]


conf = Settings()
