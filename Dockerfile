FROM ubuntu:20.04

WORKDIR /root/

### Install packages and utilities

# You may replace the URL for into a faster one in your region.
# RUN sed -i 's/archive.ubuntu.com/ftp.daumkakao.com/g' /etc/apt/sources.list
ENV DEBIAN_FRONTEND="noninteractive"

RUN apt-get update && \
    apt-get -yy install \
      wget apt-transport-https git unzip \
      build-essential libtool libtool-bin gdb \
      automake autoconf bison flex python sudo vim \
      curl software-properties-common \
      python3 python3-pip libssl-dev pkg-config libffi-dev\
      libsqlite3-0 libsqlite3-dev apt-utils locales \
      python-pip-whl libleveldb-dev python3-setuptools \
      python3-dev pandoc python3-venv \
      libgmp-dev libbz2-dev libreadline-dev libsecp256k1-dev locales-all
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get -yy install nodejs
RUN locale-gen en_US.UTF-8
RUN python3 -m pip install -U pip

# Install .NET Core
RUN wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && apt-get -yy install dotnet-sdk-8.0 && \
    rm -f packages-microsoft-prod.deb
ENV DOTNET_CLI_TELEMETRY_OPTOUT=1

# Install truffle, web3, ganache-cli
RUN npm install -g truffle web3 ganache-cli

# Install opam
RUN add-apt-repository ppa:avsm/ppa && \
    apt-get update -y && \
    apt-get -yy install opam ocaml ocaml-findlib

# Install Solidity compiler
WORKDIR /usr/bin
RUN wget https://github.com/ethereum/solidity/releases/download/v0.4.25/solc-static-linux
RUN mv solc-static-linux solc
RUN chmod +x solc

WORKDIR /root

### Prepare a user account

RUN useradd -ms /bin/bash test
RUN usermod -aG sudo test
RUN echo "test ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers
USER test
WORKDIR /home/test

### Install smart contract testing tools
RUN mkdir /home/test/tools

# Install SmarTest
COPY --chown=test:test ./docker-setup/SmarTest/ /home/test/tools/SmarTest
RUN /home/test/tools/SmarTest/install_SmarTest.sh

# # Install rlf
COPY --chown=test:test ./docker-setup/rlf/ /home/test/tools/rlf/
RUN cd /home/test/tools/rlf && \
    wget https://dl.google.com/go/go1.10.4.linux-amd64.tar.gz && \
    tar -xvf go1.10.4.linux-amd64.tar.gz && \
    sudo cp -r /home/test/tools/rlf/go /usr/lib/go-1.10
ENV GOPATH=/home/test/tools/rlf/go
ENV GOROOT=/usr/lib/go-1.10
ENV PATH=$PATH:$GOPATH/bin:$GOROOT/bin
RUN /home/test/tools/rlf/install_rlf.sh

# Install ilf
COPY --chown=test:test ./docker-setup/ilf/ /home/test/tools/ilf
ENV GOPATH=/home/test/tools/ilf/go
ENV GOROOT=/usr/lib/go-1.10
ENV PATH=$PATH:$GOPATH/bin
ENV PATH=$PATH:$GOROOT/bin
RUN /home/test/tools/ilf/install_ilf.sh
RUN mv /home/test/tools/ilf/preprocess \
       /home/test/tools/ilf/go/src/ilf/preprocess


# Install Smartian
RUN cd /home/test/tools/ && \
    git clone https://github.com/SoftSec-KAIST/Smartian.git && \
    cd Smartian && \
    git checkout 8b45b6f && \
    git submodule update --init --recursive && \
    make

# Install IConFuzz
RUN cd /home/test/tools/ && \
    git clone https://github.com/infosec-sogang/IConFuzz.git && \
    cd IConFuzz && \
    git checkout fc6337afeba09e3354219daca6b79124035d8d7c && \
    git submodule update --init --recursive && \
    make

# Add scripts for each tool
COPY --chown=test:test ./docker-setup/tool-scripts/ /home/test/scripts

### Prepare benchmarks

COPY --chown=test:test ./benchmarks /home/test/benchmarks

CMD ["/bin/bash"]
