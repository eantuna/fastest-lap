FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get -y --no-install-recommends install \
    build-essential \
    ca-certificates \
    cmake \
    curl \
    gfortran \
    git \
    liblapack-dev \
    pkgconf

WORKDIR /opt

RUN git clone https://github.com/juanmanzanero/fastest-lap.git

WORKDIR /opt/fastest-lap/build

RUN cmake .. -DPYTHON_API_ABSOLUTE_PATH=off && \
    make

# RUN mkdir cli
# COPY src/test/cli/f1_optimal_laptime.cpp cli/f1_optimal_laptime.cpp
# WORKDIR /opt/fastest-lap/build/cli
# RUN g++ -o f1_optimal_laptime -I/opt/fastest-lap/build/thirdparty/include -I/opt/fastest-lap/build/lion/build/lion/thirdparty/include -I/opt/fastest-lap -v f1_optimal_laptime.cpp -L/opt/fastest-lap/build/thirdparty/lib -lblas -llapack -ltinyxml2 -L/opt/fastest-lap/build/lib -lfastestlapc