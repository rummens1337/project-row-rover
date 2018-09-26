# Rover

Robot On Wheels (ROW) rover, geschreven in Python door Noeël Moeskops, Robin de Jong, Michel Rummens en Robin Vonk. Project voor de Hogeschool van Amsterdam 2018, 2e jaar Techniche Informatica.

[Docker Hub](https://hub.docker.com/r/noeel/rover/)

# Install/update
**Note - werkt alleen op een ARM systeem!**

1) Download [Docker](https://docs.docker.com/install/#supported-platforms).

2) Run `docker pull noeel/rover:latest` om de image te downloaden/updaten.

3) Run `docker run --device /dev/gpiomem noeel/rover:latest --restart always` om hem uittevoeren en bij reboot/crash opnieuw optestarten.

# Make dev-env
Omdat dit project is gemaakt voor een raspberry Pi 3 met een ARM processor en GPIO pins moeten deze worden geemuleerd worden in een x86 architectuur.

1) Download [Docker](https://docs.docker.com/install/#supported-platforms).

2) Run `make install` op een niet ARM architectuur om een qemu emulator te installeren op je systeem.

3) Run `make build` om een docker image te crearen van deze repo.

4) Run `make run-amd64` om het de docker image uittevoeren (`make run` op een apparaat met GPIO pins). Wanneer je de applictie wilt updaten met je aanpassingen in deze map kan je ook alleen `make run-current(-amd64)` zodat je niet altijd docker opnieuw hoeft te bouwen. Wanneer je een ander bestand dan `main.py` wilt uitvoeren kan je dat doormiddel van de `target` parameter doen (`make run-current-amd64 target=src/hardware/camera.py`).

# Config

in `./settings.conf` staat alle confugiratie voor productie (ARM RPi), in `./settings.amd64.conf` kan je je instellingen aanpassen voor de dev builds.

# Push to docker

1) login op Docker.

2) Run `make push` optioneel tag parameter (`make push tag=1.1`)

# How to use

1) Start de applicatie op een RPi.

2) Verbind met je favorite apparaat met de david-rover wifi

3) ???

4) profit!
