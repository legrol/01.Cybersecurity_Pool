FROM alpine:latest
LABEL maintainer="inquisitor"

RUN set -ex && apk add --update --no-cache net-tools arping python3 py3-pip openssh-server

ENV VENV_PATH=/opt/inquisitor-venv
ENV PATH="$VENV_PATH/bin:$PATH"

COPY requirements.txt /tmp/
RUN echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config
RUN echo 'Port 4242' >> /etc/ssh/sshd_config
# COPY sshd_config /etc/ssh/sshd_config
COPY entrypoint.sh /entrypoint.sh

RUN set -ex && python3 -m venv "$VENV_PATH" && \
    "$VENV_PATH/bin/pip" install --upgrade pip && \
    "$VENV_PATH/bin/pip" install --requirement /tmp/requirements.txt && \
    chmod +x /entrypoint.sh 
    # && \     echo "root:root" | chpasswd

WORKDIR /usr/src/

EXPOSE 4242

ENTRYPOINT ["/entrypoint.sh"]

