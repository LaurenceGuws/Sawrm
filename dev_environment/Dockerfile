# # Load the environment variables
# Get-Content .\.env | ForEach-Object { $key, $value = $_.Split('='); [Environment]::SetEnvironmentVariable($key, $value, [EnvironmentVariableTarget]::Process) }

# # Build the Docker image
# docker build --build-arg GIT_EMAIL=$Env:GIT_EMAIL --build-arg GIT_USERNAME=$Env:GIT_USERNAME --build-arg GIT_TOKEN=$Env:GIT_TOKEN -t dev_environment .

# $Env:PYTHONPATH += ";C:\Repos\POC's\Swarm"

# Set up a git account for the swarm.
# Use an official Ubuntu as a base image
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
