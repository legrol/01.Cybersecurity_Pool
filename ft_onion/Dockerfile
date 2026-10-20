FROM debian:bookworm

# Instala servicios
RUN apt-get update && apt-get install -y \
    nginx \
    openssh-server \
    tor \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Usuario de prueba para evaluación SSH
RUN useradd -m -s /bin/bash evaluator && \
    echo 'evaluator:evaluator42' | chpasswd

# Crea directorios necesarios
RUN mkdir -p /var/run/sshd /var/lib/tor/onion_web_service

# Copia configuraciones
COPY nginx.conf /etc/nginx/nginx.conf
COPY sshd_config /etc/ssh/sshd_config
COPY torrc /etc/tor/torrc
COPY index.html /var/www/html/index.html

# Cambia permisos Tor
RUN chown -R debian-tor:debian-tor /var/lib/tor/onion_web_service && \
    chmod 700 /var/lib/tor/onion_web_service

# Expone puertos
EXPOSE 80 4242

# Script de inicio
RUN echo '#!/bin/bash\n\
service nginx start\n\
service ssh start\n\
service tor start\n\
echo "Servicios iniciados. Esperando..."\n\
sleep 5\n\
echo "Dirección onion:"\n\
cat /var/lib/tor/onion_web_service/hostname\n\
tail -f /dev/null' > /start.sh && chmod +x /start.sh

CMD ["/start.sh"]
