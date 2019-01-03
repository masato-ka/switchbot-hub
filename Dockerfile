FROM raspbian/stretch

MAINTAINER masato-ka <jp6uzv@gmail.com>

# setup python.
RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip

# Install application.
RUN mkdir switchbot-hub
ADD resources switchbot-hub/resources
ADD switchbot_hub switchbot-hub/switchbot_hub
ADD switchbot-hub.conf switchbot-hub
ADD constraints.txt switchbot-hub
ADD setup.py switchbot-hub
ADD setup.cfg switchbot-hub
RUN pip3 install -e ./switchbot-hub

# setup enviroment
RUN mkdir log

# Start application.
#ENTRYPOINT ["pwd"]
ENTRYPOINT ["python3", "/switchbot-hub/switchbot_hub/main.py"]


