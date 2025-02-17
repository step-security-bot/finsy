# Dockerfile that produces an ubuntu-based image with BMV2 and Mininet.

FROM docker.io/opennetworking/mn-stratum AS stratum

FROM ubuntu:22.04 AS builder
WORKDIR /root
COPY build.sh p4switch.py ./
COPY --from=stratum /stratum_bmv2_deb.deb \
  /usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.67.0 \
  /usr/lib/x86_64-linux-gnu/libboost_thread.so.1.67.0 \
  /usr/lib/x86_64-linux-gnu/libboost_system.so.1.67.0 \
  /usr/lib/x86_64-linux-gnu/libboost_program_options.so.1.67.0 \
  /usr/lib/x86_64-linux-gnu/libboost_atomic.so.1.67.0 \
  ./stratum/
RUN ./build.sh

FROM ubuntu:22.04
ARG BMV2_DEPS="libpcap0.8 libboost-filesystem1.74.0 libboost-program-options1.74.0 libboost-thread1.74.0"
ARG MININET_DEPS="python3 net-tools iproute2 iputils-ping socat psmisc procps ethtool iperf tcpdump telnet"
ARG OTHER_DEPS="python3-venv"
ARG STRATUM_DEPS="libjudydebian1"
COPY --from=builder /output /usr/local/
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -qq update \
    && apt-get -y --no-install-recommends install $BMV2_DEPS $MININET_DEPS $OTHER_DEPS $STRATUM_DEPS \
    && rm -rf /var/lib/apt/lists/* \
    && ldconfig \
    && ln -s /usr/local/stratum/etc /etc/stratum

LABEL org.opencontainers.image.description="This image runs Mininet with a P4Runtime switch (bmv2 or stratum_bmv2)."
EXPOSE 50001-50999
ENTRYPOINT ["mn", "--custom", "/usr/local/mininet/custom/p4switch.py", "--switch", "bmv2", "--controller", "none"]
