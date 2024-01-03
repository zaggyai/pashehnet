FROM ubuntu:22.04
RUN  apt -y update && \
     apt -y upgrade
RUN  apt -y install python3 python3-pip
RUN  python3 -m pip install pashehnet
RUN useradd -ms /bin/bash pashehnet
USER pashehnet
WORKDIR /pashehnet
ENTRYPOINT ["pashehnet", "run"]
