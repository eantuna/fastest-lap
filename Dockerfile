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

# Patch Lion build
COPY cmake/third-party/custom_fixes/loggercpp.cmake /opt/fastest-lap/cmake/third-party/custom_fixes/loggercpp.cmake
COPY cmake/third-party/lion.cmake /opt/fastest-lap/cmake/third-party/lion.cmake

WORKDIR /opt/fastest-lap/build

RUN cmake .. -DPYTHON_API_ABSOLUTE_PATH=off && \
    make

RUN mkdir cli
COPY src/test/cli/f1_optimal_laptime.cpp cli/f1_optimal_laptime.cpp
COPY src/test/cli/circuit_preprocessor.cpp cli/circuit_preprocessor.cpp
WORKDIR /opt/fastest-lap/build/cli
RUN g++ -o f1_optimal_laptime -I/opt/fastest-lap/build/thirdparty/include -I/opt/fastest-lap/build/lion/build/lion/thirdparty/include -I/opt/fastest-lap -v f1_optimal_laptime.cpp -L/opt/fastest-lap/build/thirdparty/lib -lblas -llapack -ltinyxml2 -L/opt/fastest-lap/build/lib -lfastestlapc
RUN g++ -o f1_circuit_preprocessor -I/opt/fastest-lap/build/thirdparty/include -I/opt/fastest-lap/build/lion/build/lion/thirdparty/include -I/opt/fastest-lap -v circuit_preprocessor.cpp -L/opt/fastest-lap/build/thirdparty/lib -lblas -llapack -ltinyxml2 -L/opt/fastest-lap/build/lib -lfastestlapc
ENV LD_LIBRARY_PATH=/opt/fastest-lap/build/lib:/opt/fastest-lap/build/thirdparty/lib
CMD ["./f1_optimal_laptime"]