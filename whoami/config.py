import os


CONFIG = {
    "WHOAMI_ENV": os.environ["WHOAMI_ENV"],
    "WHOAMI_PASSWORD": os.environ["WHOAMI_PASSWORD"],
    "WHOAMI_USERNAME": "whoami",
    "WHOAMI_DIR": os.path.join(os.getcwd()),
    "WHOAMI_DB_NAME": "whoami.db",
    "WHOAMI_ASSETS_DIR": "assets",
}


globals().update(**CONFIG)
