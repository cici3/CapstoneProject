ARG IMAGE_VARIANT=slim-buster
ARG OPENJDK_VERSION=8
ARG PYTHON_VERSION=3.8

FROM python:${PYTHON_VERSION}-${IMAGE_VARIANT} AS py3
FROM openjdk:${OPENJDK_VERSION}-${IMAGE_VARIANT}

COPY --from=py3 / /

ARG PYSPARK_VERSION=3.1.2
RUN pip --no-cache-dir install pyspark==${PYSPARK_VERSION}

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV DISPLAY=:99

# # Install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app
# ENV JAVA_HOME="/usr/lib/jvm/java-8-openjdk"
ENTRYPOINT python modelgenerator.py