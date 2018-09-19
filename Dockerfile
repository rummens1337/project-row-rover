FROM python:3.7

FROM mohaseeb/raspberrypi3-python-opencv:3.4.2
#FROM jjanzic/docker-python3-opencv

#COPY qemu-arm-static /usr/bin/

LABEL maintainer "Noeël Moeskops <noeel.moeskops@hva.nl>"

# Set the working directory to /app
WORKDIR /app

# compile cross-platform

ADD /src /app/src
ADD /web /app/web
ADD config.ini /app

# Install any needed packages specified in requirements.txt
#RUN pip install --trusted-host pypi.python.org -r Requirements.txt

# Define environment variable
ENV NAME rover

# Run app.py when the container launches
CMD ["python", "src/main.py"]
