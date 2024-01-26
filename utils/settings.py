import google.ai.generativelanguage as glm

function_declarations = [
    glm.FunctionDeclaration(
        name='test_connection',
        description="Send data to the test_connection function to check for the server response.",
        parameters=glm.Schema(
            type=glm.Type.OBJECT,
            properties={
                'data': glm.Schema(type=glm.Type.STRING, description="Any test data.")
            },
            required=['data']
        )
    ),
    glm.FunctionDeclaration(
        name='execute_commands',
        description="Send commands/cli commands to the execute_commands function to be run. Use this function to access your development server. You can do anying to your server that the task requires.",
        parameters=glm.Schema(
            type=glm.Type.OBJECT,
            properties={
                'commands': glm.Schema(
                    type=glm.Type.ARRAY,
                    description="List of shell commands to execute_commands. eg. ls, mkdir, pip install, git clone https://github.com/GooseSAndboxx/DevEnvironment, git add file  etc."
                )
            },
            required=['commands']
        )
    ),
    glm.FunctionDeclaration(
        name='write_file',
        description="Use the write_file function to send data to the development server as a file. It can also be used to write code to aid in solveing complex tasks like math. you can write a python script, and add another function call to execute the file.",
        parameters=glm.Schema(
            type=glm.Type.OBJECT,
            properties={
                'operations': glm.Schema(
                    type=glm.Type.ARRAY,
                    description="List of file operation objects, each specifying 'data', 'file_name', and 'file_path'.",
                    items=glm.Schema(
                        type=glm.Type.OBJECT,
                        properties={
                            'data': glm.Schema(type=glm.Type.STRING, description="Content to be written to the file."),
                            'file_name': glm.Schema(type=glm.Type.STRING, description="The name of the file to write to with extension."),
                            'file_path': glm.Schema(type=glm.Type.STRING, description="The path to the directory where the file will be written."),
                        },
                        required=['data', 'file_name', 'file_path']
                    )
                )
            },
            required=['operations']
        )
    )
]

safety_settings=[
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
    ]

history=[
    {
      "role": "user",
      "parts": [
          '''
            Your position is software_developer
            Here is the code for your server
            FROM ubuntu:latest

            # Install Python
            RUN apt-get update && apt-get install -y python3 python3-pip && apt-get install -y sudo && apt-get install -y curl && apt-get install -y wget
            # Set Python 3 as the default
            RUN ln -s /usr/bin/python3 /usr/bin/python

            # Install Git, Java, and other useful tools
            RUN apt-get install -y git

            # Set Git configuration
            ARG GIT_EMAIL
            ARG GIT_USERNAME
            RUN git config --global user.email $GIT_EMAIL
            RUN git config --global user.name $GIT_USERNAME

            # Set Git to store credentials and hardcode the GitHub token
            ARG GIT_TOKEN
            RUN git config --global credential.helper store && \
                echo "https://$GIT_USERNAME:$GIT_TOKEN@github.com" > /root/.git-credentials

            # Set the working directory in the container
            WORKDIR /usr/src/app

            # Copy the current directory contents into the container at /usr/src/app
            COPY . .

            # Install any needed packages specified in requirements.txt
            RUN pip install --no-cache-dir -r requirements.txt

            # Make port 5000 available to the world outside this container
            EXPOSE 5000
            # Define environment variable
            ENV NAME World

            # Print out the environment variables
            RUN echo "GIT_EMAIL: $GIT_EMAIL"
            RUN echo "GIT_USERNAME: $GIT_USERNAME"
            RUN echo "GIT_TOKEN: $GIT_TOKEN"

            # Run hook.py when the container launches
            CMD ["python", "./hook.py"]
            
            import os
            import subprocess
            import logging
            from flask import Flask, request, jsonify

            app = Flask(__name__)

            # Configure logging
            logging.basicConfig(level=logging.INFO)

            # Global variable to store the last accessed path
            last_path = None

            @app.route('/test_connection', methods=['POST'])
            def test_connection():
                data = request.json
                print("Received data:", data)
                return jsonify({"status": "success", "message": "Test connection successful!"}), 200




            @app.route('/execute', methods=['POST'])
            def execute_commands():
                global last_path
                data = request.json
                commands = data.get("commands", [])
                logging.info("Executing commands: %s", commands)

                results = []
                for command in commands:
                    try:
                        if last_path and os.path.isdir(last_path):
                            os.chdir(last_path)

                        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        output, error = process.communicate()

                        if command.startswith('cd '):
                            last_path = command[3:]

                        status = "failure" if process.returncode != 0 else "success"
                        results.append({"command": command, "status": status, "output": output, "error": error})
                    except subprocess.CalledProcessError as e:
                        results.append({"command": command, "status": "failure", "error": str(e)})
                return jsonify(results), 200

            @app.route('/write-file', methods=['POST'])
            def write_files():
                operations = request.json.get("operations", [])
                logging.info("File operations: %s", operations)

                results = []
                for op in operations:
                    file_content = op.get("data")
                    file_name = op.get("file_name")
                    file_path = op.get("file_path") or '.'
                    file_path = file_path.replace('\\', '/')
                    full_path = os.path.join(file_path, file_name)

                    try:
                        if file_path != '.':
                            os.makedirs(file_path, exist_ok=True)

                        with open(full_path, 'w') as file:
                            file.write(file_content)

                        results.append({"file_name": file_name, "file_path": file_path if file_path != '.' else '', "status": "success"})
                    except Exception as e:
                        results.append({"file_name": file_name, "file_path": file_path if file_path != '.' else '', "error": str(e), "status": "failure"})
                        return jsonify(results), 500
                return jsonify(results), 200

            if __name__ == '__main__':
                app.run(host='0.0.0.0', port=5000)

          You can use this environment with your tools.
          '''
      ]
    },
    {
      "role": "model",
      "parts": ["Understood, I'm a software_developer. I'll build perfect aplications with this development environment."]
    },
    {
      "role": "user",
      "parts": ['''
                System Update: Communication Protocol

                Effective immediately, please prepend your role title to all messages. Example: "[Front-End Developer]: UI issue resolved." This ensures clarity in our inter-role communications.

                Thank you for your cooperation.

                '''
                ]
    },
    {
      "role": "model",
      "parts": ["software_developer: Understood."]
    },
]
