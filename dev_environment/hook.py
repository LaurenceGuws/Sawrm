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
