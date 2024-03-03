import os
import secrets

ENVIRON = os.environ.get("ENVIRON", "PRODUCTION")
DEBUG = True if os.environ.get("DEBUG", "True") == "True" else False
IN_DOCKER = True if os.environ.get("IN_DOCKER", False) == "True" else False

BASE_PATH = os.environ.get("ABSA_AND_OPINION_MINING_API", "/home/user/Projects/absa_and_opinion_mining_api")
BASE_DATA_PATH = os.environ.get("ABSA_AND_OPINION_MINING_API_DATA",
                                "/home/user/Projects/absa_and_opinion_mining_api/absa_and_opinion_mining_api_data")

SESSION_KEY = secrets.token_hex(8)
print(f"connecting to the {ENVIRON} database")
print("CurrentSessionKey:", SESSION_KEY)
print("DEBUG:", DEBUG)
print("IN_DOCKER:", IN_DOCKER)

HOST = "0.0.0.0"
APP_MAIN_PORT = int(os.environ.get("APP_MAIN_PORT", 80))

DEFAULT_LANGUAGE = "en"

# PRODUCTION DATABASE CONNECTION CREDENTIAL
# host and port declared here wont be used before the project uses DSN for connection
# server, port and db are specified in odbcinst.ini
#
# if ENVIRON == "LOCAL":
#     MSSQL_AUTH = {"r": {
#         "username": "appuser",
#         "password": r"Locobuzz@123",
#         "db_name": "Spatialrss"
#     },
#         "rw": {
#             "username": "appuser",
#             "password": r"Locobuzz@123",
#             "db_name": "Spatialrss"
#         }
#     }
# elif ENVIRON in ["DEVELOPMENT", "PRODUCTION"]:
#     MSSQL_AUTH = {"r": {
#         "username": "RDUBSU6KMWWn3DQZNNzG_AI_Application",
#         "password": r">\Wt<C}H&[$222TEp`5krrZ```",
#         "db_name": "Spatialrss"
#     },
#         "rw": {
#             "username": "RDUBSU6KMWWn3DQZNNzG_AI_Application",
#             "password": r">\Wt<C}H&[$222TEp`5krrZ```",
#             "db_name": "Spatialrss"
#         }}
# else:
#     raise ValueError("Unknown ENVIRON")
