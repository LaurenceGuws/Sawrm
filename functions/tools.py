import proto
import requests
from utils import utils

# Configure logger
logger = utils.setup_logging()
BASE_URL = "http://localhost:5000"  # Update if your server URL differs
# BASE_URL = "https://8afa-105-242-65-118.ngrok-free.app"  # Update if your server URL differs

def test_connection(data):
    try:
        logger.debug("Executing test_connection command")
        response = requests.post(f"{BASE_URL}/test_connection", json=data)
        logger.debug("Response from test_connection: %s", response.json())
        return {"fc_name": "test_connection", **response.json()}
    except Exception as e:
        logger.error("test_connection error: %s", e)
        return {"fc_name": "test_connection", "error": str(e)}

def execute_commands(commands):
    try:
        logger.debug("Executing execute_commands")
        
        if isinstance(commands, proto.marshal.collections.repeated.RepeatedComposite):
            commands = list(commands)

        data = {"commands": commands}
        response = requests.post(f"{BASE_URL}/execute", json=data)
        logger.debug("Response from execute: %s", response.json())

        response_data = response.json()
        if isinstance(response_data, list):
            return {"fc_name": "execute_commands", "response": response_data}
        else:
            return {"fc_name": "execute_commands", **response_data}
    except Exception as e:
        logger.error("Execute commands error: %s", e)
        return {"fc_name": "execute_commands", "error": str(e)}



def write_file(operations):
    try:
        logger.debug("Executing write_file")
        data = {"operations": operations}
        response = requests.post(f"{BASE_URL}/write-file", json=data)
        logger.debug("Response from write-file: %s", response.json())

        response_data = response.json()
        if isinstance(response_data, list):
            return {"fc_name": "write_file", "response": response_data}
        else:
            return {"fc_name": "write_file", **response_data}
    except Exception as e:
        logger.error("Write file error: %s", e)
        return {"fc_name": "write_file", "error": str(e)}


