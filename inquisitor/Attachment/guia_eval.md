# Guía de evaluación - Inquisitor (paso a paso)

Documento pensado para seguir exactamente la evaluación del subject/rúbrica.

## 0) Preparación antes de evaluar (42)

1. Clonar repo en directorio vacío.
2. Verificar que corresponde al proyecto correcto.
3. Levantar entorno sin intervención manual:

```bash
make down && make up && make ps
```

4. Confirmar contenedores:

```bash
make ps
```

5. Identificar IP/MAC de gateway, atacante y víctima con `docker inspect`.

---

## 1) Criterios de corte (si falla, detener evaluación)

Detener y marcar fallo si ocurre alguno de estos puntos:

- No funciona con IPv4 de forma correcta.
- No hace poisoning en ambos sentidos.
- No redirige tráfico.
- No restaura ARP al detener.
- No detecta tráfico FTP de control (port 21).
- No detecta nombres de archivos en `STOR/RETR`.
- Excepción no controlada / parada inesperada del programa.

---

## 2) Ejecución del programa

En T1 (host), obtener parámetros reales:

```bash
SRC="$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}} {{.MacAddress}}{{end}}' ftp_server)"
SRC_IP="$(echo "$SRC" | awk '{print $1}')"
SRC_MAC="$(echo "$SRC" | awk '{print $2}')"

TGT="$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}} {{.MacAddress}}{{end}}' user)"
TGT_IP="$(echo "$TGT" | awk '{print $1}')"
TGT_MAC="$(echo "$TGT" | awk '{print $2}')"
```

Ejecutar en atacante:

```bash
docker exec -it poison python3 -u /usr/src/inquisitor.py "$SRC_IP" "$SRC_MAC" "$TGT_IP" "$TGT_MAC" -i eth0 -v
```

Ejemplo:

```bash
python3 inquisitor.py 172.22.0.1 aa:bb:cc:dd:ee:01 172.22.0.10 aa:bb:cc:dd:ee:10 -i eth0 -v
```

Esperado:

- El proceso queda activo (no termina solo).
- Muestra inicio de sniffing FTP.
- No revienta ante entradas válidas.

---

## 3) Prueba A - ARP poisoning full duplex

### Paso A1: comprobar envenenamiento en víctima

En víctima/gateway revisar tabla ARP (`/proc/net/arp`).

Esperado:

- La IP del otro extremo apunta temporalmente a la MAC del atacante.

### Paso A2: verificar ambos sentidos

Comprobar que tanto víctima como gateway reciben entradas ARP envenenadas.

Esperado:

- Poisoning en ambos lados (full duplex), no solo uno.

---

## 4) Prueba B - redirección de tráfico

Generar tráfico entre víctima y gateway (ping/FTP).

Esperado:

- El tráfico sigue funcionando (MITM reenviando), no se corta conectividad.
- Si hay captura, se observa paso por atacante.

---

## 5) Prueba C - sniffing FTP y nombres de archivos

En T2 (host), ejecutar:

```bash
docker exec user sh -c "set -e; echo 'hola evaluacion' > /tmp/prueba_subida.txt; lftp -u ftpuser,ftppass ftp_server -e 'set xfer:clobber true; put /tmp/prueba_subida.txt -o prueba_subida.txt; get prueba_subida.txt -o /tmp/prueba_bajada.txt; bye'; ls -l /tmp/prueba_bajada.txt; head -n 1 /tmp/prueba_bajada.txt"
```

Si aparece `553`/`550`, ejecutar una vez y repetir:

```bash
docker exec ftp_server sh -c 'mkdir -p /home/vsftpd/ftpuser /srv && chmod 777 /home/vsftpd /home/vsftpd/ftpuser /srv'
```

Esperado en salida de Inquisitor (T1):

- `[FTP][UPLOAD] prueba_subida.txt`
- `[FTP][DOWNLOAD] prueba_subida.txt`

Validación clave:

- Debe detectar comandos en puerto 21.
- Debe mostrar nombres de archivo en tiempo real.

---

## 6) Prueba D - restauración al parar

Detener programa con `CTRL+C`.

Esperado:

- Mensaje de restauración ARP.
- Tablas ARP de víctima/gateway vuelven a MAC reales.
- Sin cierre abrupto ni error no controlado.

---

## 7) Prueba E - manejo de errores de entrada

Lanzar ejemplos inválidos:

```bash
python3 inquisitor.py 999.1.1.1 aa:bb:cc:dd:ee:ff 10.0.0.2 11:22:33:44:55:66
python3 inquisitor.py 10.0.0.1 zz:zz:zz:zz:zz:zz 10.0.0.2 11:22:33:44:55:66
```

Esperado:

- Error claro y salida controlada.
- Nunca caída inesperada.

---

## 8) Checklist final de corrección

- [ ] 4 parámetros mínimos requeridos
- [ ] Solo IPv4
- [ ] Poisoning full duplex
- [ ] Redirección de tráfico activa
- [ ] Restauración ARP al detener
- [ ] Sniffing FTP port 21
- [ ] Detección de archivos `STOR/RETR`
- [ ] Excepciones controladas
- [ ] Sin parada inesperada

---

## 9) Nota para la defensa oral

Explicar claramente:

- Qué IP/MAC representa cada argumento.
- Cómo se consigue MITM con ARP en ambos sentidos.
- Por qué hay que activar `ip_forward`.
- Cómo se detectan `STOR/RETR` en FTP control.
- Cómo y cuándo se restaura ARP.
