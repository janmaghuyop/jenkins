# syntax=docker/dockerfile:1.4.3
# DO NOT REMOVE FIRST LINE, ENABLE BUILDKIT





# https://hub.docker.com/r/jenkins/jenkins/tags
FROM docker.io/jenkins/jenkins:2.361.1-lts-alpine AS jenkins

ENV  JAVA_OPTS -Djenkins.install.runSetupWizard=false
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli -f /usr/share/jenkins/ref/plugins.txt





FROM docker.io/python:3.9-alpine AS secrets
RUN pip install --no-cache-dir requests
COPY serve-secrets.py .





# https://registry.hub.docker.com/r/jenkins/jnlp-slave/tags
FROM docker.io/jenkins/jnlp-slave:4.13.3-1-jdk11 AS slave
USER root
RUN apt update && \
    apt install -y curl jq
USER jenkins

