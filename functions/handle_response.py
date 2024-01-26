import collections
import google.ai.generativelanguage as glm

from functions.tools import execute_commands, test_connection, write_file
from utils import utils
logger = utils.setup_logging()

import proto  # Ensure this module is imported

def extract_function_calls(response):
    function_calls = []
    logger.info("Extracting function calls from the response")
    logger.debug(response.candidates)  # Detailed logging of the response

    for candidate in response.candidates:
        for part in candidate.content.parts:
            if hasattr(part, 'function_call'):
                fc = part.function_call
                fc_name = fc.name
                fc_args = {}
                # Convert MapComposite to a regular dictionary
                args_dict = dict(fc.args) if isinstance(fc.args, proto.marshal.collections.maps.MapComposite) else {}
                logger.debug(f"args_dict: {args_dict}")
                if fc_name == "write_file":
                    new_args = {}
                    if 'operations' in args_dict:
                        # Process each MapComposite object in the operations list
                        new_args['operations'] = []
                        for operation_comp in args_dict['operations']:
                            if isinstance(operation_comp, proto.marshal.collections.maps.MapComposite):
                                operation_dict = dict(operation_comp)
                                new_args['operations'].append(operation_dict)
                            else:
                                logger.warning(f"Non-MapComposite item found in operations: {operation_comp}")
                    else:
                        logger.warning("'operations' key not found or not a list in args_dict")
                    logger.debug(f"new_args: {new_args}")
                    for key, value in new_args.items():
                        fc_args[key] = extract_operations(value)
                        logger.debug(f"Extracted operations for write_file: {fc_args[key]}")

                # Process each argument
                for key, value in args_dict.items():
                    if fc_name in ['test_connection', 'execute_commands']:
                        if key == 'commands':
                            logger.debug(f"Type of 'commands': {type(value)}")
                            if isinstance(value, collections.abc.Sequence) and not isinstance(value, str):
                                fc_args[key] = value
                                logger.debug(f"Extracted commands for {fc_name}: {fc_args[key]}")
                            else:
                                logger.warning(f"Unexpected format for 'commands': {value}")
                        else:
                            fc_args[key] = value
                            logger.debug(f"Extracted {key} for {fc_name}: {fc_args[key]}")



                function_calls.append((fc_name, fc_args))
    logger.info(f"Extracted function calls: {function_calls}")
    processed_calls = process_function_calls(function_calls)
    logger.info(f"process_function_calls: {processed_calls}")
    return function_calls

def extract_operations(operations_list):
    operations = []
    logger.debug("Extracting operations from the value")

    # Check if operations_list is actually a list of dictionaries
    if isinstance(operations_list, list) and all(isinstance(op, dict) for op in operations_list):
        for operation in operations_list:
            op_data = {}
            for op_key, op_value in operation.items():
                # Assuming all values are already string or compatible types
                op_data[op_key] = op_value
            operations.append(op_data)
            logger.debug(f"Extracted operation: {op_data}")
    else:
        logger.warning("Invalid format for operations list. Expected a list of dictionaries.")

    logger.debug(f"Final extracted operations: {operations}")
    return operations


def process_function_calls(function_calls):
    responses = []
    logger.info("Processing function calls")

    if not function_calls or all(fc_name == '' for fc_name, _ in function_calls):
        logger.info("No valid function calls to process.")
        return function_calls
    
    for fc_name, fields in function_calls:
        try:
            if fc_name == 'test_connection':
                data = {field: value for field, value in fields.items()}
                response = test_connection(data)
                logger.debug(f"Processed test_connection with data: {data}")

            elif fc_name == 'execute_commands':
                commands = fields.get('commands', [])
                response = execute_commands(commands)
                logger.debug(f"Processed execute_commands with commands: {commands}")

            elif fc_name == 'write_file':
                operations = fields.get('operations', [])
                response = write_file(operations)
                logger.debug(f"Processed write_file with operations: {operations}")

            else:
                raise ValueError(f"Unknown function call: {fc_name}")

            responses.append(response)

        except Exception as e:
            logger.error(f"Error processing {fc_name}: {e}", exc_info=True)
            responses.append({"error": str(e)})

    logger.info(f"Final processed responses: {responses}")
    return responses
