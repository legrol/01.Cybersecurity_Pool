# Chuleta defensa (20-30s)

## Guion oral corto

- Este proyecto hace ARP poisoning full duplex entre víctima y servidor/gateway.
- El tráfico pasa por el contenedor atacante (`poison`) y se mantiene conectividad.
- Se captura control FTP por puerto 21 y se detectan comandos `STOR`/`RETR`.
- En tiempo real se muestran nombres de archivos subidos y descargados.
- Al pulsar `Ctrl+C`, el programa restaura tablas ARP en ambos lados.
- Solo acepta IPv4 y valida entrada para evitar errores no controlados.

## Checklist final de evaluación (sí/no)

- [ ] Arranca entorno con `make down && make up && make ps`
- [ ] Obtiene IP/MAC reales con `docker inspect`
- [ ] Ejecuta `inquisitor.py` sin cierre inesperado
- [ ] ARP poisoning visible en `/proc/net/arp`
- [ ] FTP `put/get` funciona
- [ ] En T1 aparecen `[FTP][UPLOAD]` y `[FTP][DOWNLOAD]`
- [ ] `Ctrl+C` restaura ARP
- [ ] Sin excepciones no controladas

## Comandos de cierre

```bash
# T1
Ctrl+C

# T2
docker exec user cat /proc/net/arp
docker exec ftp_server cat /proc/net/arp
```
