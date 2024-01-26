import google.generativeai as genai
import google.ai.generativelanguage as glm

import handle_response
from utils import settings
from configparser import ConfigParser

config = ConfigParser()
config.read('conf\.env')

API_KEY = config['DEFAULT']['API_KEY']
genai.configure(api_key=API_KEY)
safety_settings=settings.safety_settings
history=settings.history #This will be custom for each agent, teaching it how to recieve and respond with messages.
tool = glm.Tool(function_declarations=settings.function_declarations)
tools = [tool]
model = genai.GenerativeModel('gemini-pro', tools=tools, safety_settings=safety_settings)
convo = model.start_chat(history=history)


def chat(prompt, convo):
    # Fix this sippet
    chat = convo

    response = chat.send_message(prompt, safety_settings=settings.safety_settings)
    while True:

        tools_response = handle_response.extract_function_calls(response)

        parts = []
        if any(fc_name for fc_name, _ in tools_response):
            for tool_response in tools_response:
                # Unpack the tuple
                fc_name, response_data = tool_response

                # Only process if fc_name is not empty
                if fc_name:
                    # Build the glm.Part for each tool response
                    parts.append(
                        glm.Part(
                            function_response=glm.FunctionResponse(
                                name=fc_name,
                                response=response_data
                            )
                        )
                    )

        # Send all tool responses back in one message
        if parts:
            response = chat.send_message(glm.Content(parts=parts))
            print(response.candidates)
        else:
            print(response.candidates)
            break



while True:
        # Get user input
        user_input = input("Enter your command: ")
        # Example usage
        prompt = "Your prompt here"
        chat(user_input, convo)
