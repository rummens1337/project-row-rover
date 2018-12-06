# TODO dit heeft alleen maar python 3.5, we moeten zelf een image maken met 3.7
FROM sgtwilko/rpi-raspbian-opencv:stretch-3.4.3

RUN adduser -u 1000 --system --group --shell /bin/sh rover

# compile cross-platform
COPY qemu-arm-static /usr/bin/

COPY Requirements.txt /app/Requirements.txt

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY settings.template.conf /app/settings.conf

LABEL maintainer "Noeël Moeskops <noeel.moeskops@hva.nl>"

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r Requirements.txt

# Install supervisor, requered for multiprocessing
RUN apt-get update && apt-get install -y supervisor=3.3.1-1+deb9u1 alsa-utils espeak python3-espeak

RUN mkdir /appdata

RUN chown -R rover:rover /appdata


ADD /src /app/src
ADD /web /app/web
ADD /haarCascades /app/haarCascades
ADD main.py /app
ADD video_stream.py /app
ADD init.py /app

EXPOSE 80
EXPOSE 8080
# Define environment variable
ENV NAME rover

# Run main.py and /src/video_stream.py via supervisord when the container launches
CMD ["sh", "-c", "python3 init.py && supervisord"]
