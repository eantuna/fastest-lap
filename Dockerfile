FROM ubuntu:noble

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

WORKDIR /opt/fastest-lap

COPY cmake/ cmake/
COPY database/ database/
COPY src/ src/
COPY CMakeLists.txt CMakeLists.txt

WORKDIR /opt/fastest-lap/build

RUN cmake .. -DPYTHON_API_ABSOLUTE_PATH=off && \
    make

ENV PATH=/opt/fastest-lap/build/bin:$PATH

CMD ["f1_optimal_laptime"]