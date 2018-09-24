# TODO dit heeft alleen maar python 3.4, we moeten zelf een image maken met 3.7
FROM sgtwilko/rpi-raspbian-opencv:stretch-latest


# compile cross-platform
COPY qemu-arm-static /usr/bin/

LABEL maintainer "Noeël Moeskops <noeel.moeskops@hva.nl>"

# Set the working directory to /app
WORKDIR /app

ADD /src /app/src
ADD /web /app/web
ADD config.ini /app
ADD Requirements.txt /app
ADD main.py /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r Requirements.txt

# Define environment variable
ENV NAME rover

# Run app.py when the container launches
CMD ["python3", "main.py"]
