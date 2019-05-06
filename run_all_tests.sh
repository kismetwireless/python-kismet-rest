#!/bin/bash

echo "kismet.pcap file REQUIRED for testing."

echo "Testing REST SDK (Py2.7) against master branch..."

# Build Kismet container
docker build -t kismet -f ./dockerfiles/Dockerfile.kismet-app-master .

# Start Kismet container, load pcap.
docker run \
    -d \
    --name=kismet \
    --network=host \
    --cap-add=SYS_PTRACE \
    -v ${PWD}/kismet.pcap:/export/kismet.pcap \
    kismet

sleep 10

# Build testing image for Python 2.7
docker build -t testme:2.7 -f ./dockerfiles/Dockerfile.kismet-rest_2.7 .

# Run tests for Python 2.7
docker run \
    -it \
    --rm \
    --network=host \
    --name=testme_2.7 \
    testme:2.7

docker kill kismet && docker rm kismet
# exit $?

echo "Testing REST SDK (Py3.7) against master branch..."

# Build Kismet container
docker build -t kismet -f ./dockerfiles/Dockerfile.kismet-app-master .

# Start Kismet container, load pcap.
docker run \
    -d \
    --name=kismet \
    --network=host \
    --cap-add=SYS_PTRACE \
    -v ${PWD}/kismet.pcap:/export/kismet.pcap \
    kismet

sleep 10

# Build testing image for Python 3.7
docker build -t testme:3.7 -f ./dockerfiles/Dockerfile.kismet-rest_3.7 .

# Run tests for Python 3.7
docker run \
    -it \
    --rm \
    --network=host \
    --name=testme_3.7 \
    testme:3.7


# Kill and delete Kismet server container
# docker logs kismet
docker kill kismet
docker rm --force kismet

echo "Testing REST SDK (Py2.7) against current dpkg..."

# Build Kismet container
docker build -t kismet -f ./dockerfiles/Dockerfile.kismet-app .

# Start Kismet container, load pcap.
docker run \
    -d \
    --name=kismet \
    --network=host \
    --cap-add=SYS_PTRACE \
    -v ${PWD}/kismet.pcap:/export/kismet.pcap \
    kismet

sleep 10

# Build testing image for Python 2.7
docker build -t testme:2.7 -f ./dockerfiles/Dockerfile.kismet-rest_2.7 .

# Run tests for Python 2.7
docker run \
    -it \
    --rm \
    --network=host \
    --name=testme_2.7 \
    testme:2.7

docker kill kismet && docker rm kismet
# exit $?

echo "Testing REST SDK (Py3.7) against current dpkg..."

# Build Kismet container
docker build -t kismet -f ./dockerfiles/Dockerfile.kismet-app .

# Start Kismet container, load pcap.
docker run \
    -d \
    --name=kismet \
    --network=host \
    --cap-add=SYS_PTRACE \
    -v ${PWD}/kismet.pcap:/export/kismet.pcap \
    kismet

sleep 10

# Build testing image for Python 3.7
docker build -t testme:3.7 -f ./dockerfiles/Dockerfile.kismet-rest_3.7 .

# Run tests for Python 3.7
docker run \
    -it \
    --rm \
    --network=host \
    --name=testme_3.7 \
    testme:3.7


# Kill and delete Kismet server container
# docker logs kismet
docker kill kismet
docker rm --force kismet
