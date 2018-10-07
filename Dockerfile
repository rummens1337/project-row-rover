# TODO dit heeft alleen maar python 3.5, we moeten zelf een image maken met 3.7
FROM sgtwilko/rpi-raspbian-opencv:stretch-3.4.3

COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf

# compile cross-platform
COPY qemu-arm-static /usr/bin/

COPY Requirements.txt /app/Requirements.txt

LABEL maintainer "Noeël Moeskops <noeel.moeskops@hva.nl>"

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r Requirements.txt

ADD /src /app/src
ADD /web /app/web
ADD /haarCascades /app/haarCascades
ADD settings.conf /app
ADD main.py /app

EXPOSE 80

# Define environment variable
ENV NAME rover

# Run app.py when the container launches
CMD ["python3", "main.py"]
