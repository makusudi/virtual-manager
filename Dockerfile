FROM ubuntu:20.04
COPY . /opt/virtual_manager
WORKDIR /opt/virtual_manager
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get -y update
RUN apt install -y \
    gcc \
    npm \
    python3 \
    python3-dev \
    python3-pip \
    git
RUN npm install --save nuxt
RUN npm install
RUN npm run build
RUN pip3 install -r requirements.txt
RUN python3 models.py
EXPOSE 8080
ENTRYPOINT ["python3", "server.py"]
