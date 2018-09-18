# Use an official Python runtime as a parent image
FROM python:3.7

FROM jjanzic/docker-python3-opencv:latest

LABEL maintainer "Noeël Moeskops <noeel.moeskops@hva.nl>"

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r Requirements.txt

# Define environment variable
ENV NAME rover

# Run app.py when the container launches
CMD ["python", "src/main.py"]
