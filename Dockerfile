FROM jenkins/jenkins:lts-jdk17

USER root

RUN apt-get update && apt-get install -y \
    qemu-system-arm \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    wget \
    unzip \
    ipmitool \
    jq \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --break-system-packages -r /tmp/requirements.txt

USER jenkins
