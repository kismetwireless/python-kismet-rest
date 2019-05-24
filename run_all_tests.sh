#!/bin/bash
set -xe

echo "kismet.pcap file REQUIRED for testing."

docker kill kismet; docker rm kismet || echo "No Kismet server artifacts"

# Build Kismet from source
docker build -t kismet-build -f ./dockerfiles/Dockerfile.kismet-app-master .

# Build Kismet container
docker build -t kismet-package -f ./dockerfiles/Dockerfile.kismet-app .

# Build testing image for Python 2.7
docker build -t kismet-rest:2.7 -f ./dockerfiles/Dockerfile.kismet-rest_2.7 .

# Build testing image for Python 3.5
docker build -t kismet-rest:ubu16 -f ./dockerfiles/Dockerfile.kismet-rest_ubu16 .

# Build testing image for Python 3.7
docker build -t kismet-rest:3.7 -f ./dockerfiles/Dockerfile.kismet-rest_3.7 .


echo "Testing REST SDK (Ubuntu:16.04, Python 3.5) against master branch..."
# Start Kismet container, load pcap.
docker run \
    -d \
    --name=kismet \
    --network=host \
    --cap-add=SYS_PTRACE \
    -v ${PWD}/kismet.pcap:/export/kismet.pcap \
    kismet-build

sleep 15

docker run \
    -it \
    --rm \
    --network=host \
    --name=kismet-rest_ubu16 \
    kismet-rest:ubu16

docker kill kismet
docker rm --force kismet

echo "Testing REST SDK (Py2.7) against master branch..."
# Start Kismet container, load pcap.
docker run \
    -d \
    --name=kismet \
    --network=host \
    --cap-add=SYS_PTRACE \
    -v ${PWD}/kismet.pcap:/export/kismet.pcap \
    kismet-build

sleep 15

# Run tests for Python 2.7
docker run \
    -it \
    --rm \
    --network=host \
    --name=kismet-rest_2.7 \
    kismet-rest:2.7

docker kill kismet
docker rm kismet

echo "Testing REST SDK (Py3.7) against master branch..."
# Start Kismet container, load pcap.
docker run \
    -d \
    --name=kismet \
    --network=host \
    --cap-add=SYS_PTRACE \
    -v ${PWD}/kismet.pcap:/export/kismet.pcap \
    kismet-build

sleep 15

# Run tests for Python 3.7
docker run \
    -it \
    --rm \
    --network=host \
    --name=kismet-rest_3.7 \
    kismet-rest:3.7


# Kill and delete Kismet server container
# docker logs kismet
docker kill kismet
docker rm --force kismet


echo "Testing REST SDK (Py2.7) against current dpkg..."

# Start Kismet container, load pcap.
docker run \
    -d \
    --name=kismet \
    --network=host \
    --cap-add=SYS_PTRACE \
    -v ${PWD}/kismet.pcap:/export/kismet.pcap \
    kismet-package

sleep 15

# Run tests for Python 2.7
docker run \
    -it \
    --rm \
    --network=host \
    --name=kismet-rest_2.7 \
    kismet-rest:2.7

docker kill kismet && docker rm kismet
# exit $?

echo "Testing REST SDK (Py3.7) against current dpkg..."

# Start Kismet container, load pcap.
docker run \
    -d \
    --name=kismet \
    --network=host \
    --cap-add=SYS_PTRACE \
    -v ${PWD}/kismet.pcap:/export/kismet.pcap \
    kismet-package

sleep 15

# Run tests for Python 3.7
docker run \
    -it \
    --rm \
    --network=host \
    --name=kismet-rest_3.7 \
    kismet-rest:3.7


# Kill and delete Kismet server container
# docker logs kismet
docker kill kismet
docker rm --force kismet
