# Documentación técnica - Inquisitor

## 1) Objetivo del proyecto

`inquisitor.py` implementa un ataque de **ARP poisoning full duplex** entre dos nodos IPv4 (normalmente gateway y víctima), y además hace **sniffing del canal de control FTP (puerto 21)** para mostrar en tiempo real los nombres de archivos transferidos:

- `STOR <archivo>` → subida
- `RETR <archivo>` → descarga

El programa está orientado a Linux y a entorno de laboratorio (contenedor/VM), tal como exige el subject.

---

## 2) Flujo general de ejecución

1. Parsea argumentos de entrada.
2. Valida estrictamente IPv4 y MAC.
3. Intenta activar forwarding IPv4 en el host atacante (`/proc/sys/net/ipv4/ip_forward`).
4. Arranca un hilo de envenenamiento ARP continuo en ambos sentidos + ráfaga inicial (warmup).
5. Arranca sniffing de tráfico FTP en puerto 21.
6. Al recibir `CTRL+C` (SIGINT) o parada del proceso:
   - detiene el loop de poisoning,
   - restaura tablas ARP de ambos nodos con ARP legítimo.

---

## 3) Parámetros CLI

Comando base:

```bash
python3 inquisitor.py <IP-src> <MAC-src> <IP-target> <MAC-target> -i <iface> [-v]
```

### Parámetros obligatorios

- `<IP-src>`: IPv4 del origen (normalmente gateway)
- `<MAC-src>`: MAC del origen
- `<IP-target>`: IPv4 del objetivo (víctima)
- `<MAC-target>`: MAC del objetivo

### Parámetros opcionales

- `-i, --iface`: interfaz de red (por defecto la interfaz por defecto de Scapy)
- `-a, --attacker-mac`: MAC del atacante (si no se pasa, se autodetecta)
- `-v, --verbose`: salida detallada

---

## 4) Arquitectura interna del script

### `InquisitorEngine`

Clase principal que agrupa estado y operaciones:

- Estado de red: IP/MAC gateway, IP/MAC víctima, MAC atacante, interfaz
- `stop_event`: sincronización para parada limpia

### Métodos clave

- `send_fake_arp(...)`
  - Envía tramas `Ether + ARP` (`sendp`) con MAC atacante para envenenar caché ARP con más fiabilidad en Docker/bridge.
- `send_real_arp(...)`
  - Envía `Ether + ARP` legítimo (`sendp`) para restauración.
- `poisoning_loop()`
  - Envenena en ambos sentidos cada ~1s:
    - víctima cree que gateway = atacante
    - gateway cree que víctima = atacante
- `warmup_poisoning()`
  - Ráfaga inicial de ARP fake para que la primera transferencia FTP ya pase por MITM.
- `sniff_ftp_control()`
  - Captura tráfico en interfaz con `promisc=True`.
  - Filtra en Python por `TCP sport/dport 21`.
  - Reconstruye comandos por flujo para manejar fragmentación TCP (`STOR/RETR` aunque lleguen partidos).
- `restore_tables()`
  - Repara ambos lados con múltiples envíos para mayor fiabilidad.

---

## 5) Full duplex ARP poisoning (qué significa aquí)

Se falsifican simultáneamente dos relaciones:

1. Hacia la víctima: “IP del gateway está en MAC del atacante”.
2. Hacia el gateway: “IP de la víctima está en MAC del atacante”.

Con esto, el tráfico entre ambos pasa por el atacante en ambos sentidos.

---

## 6) Restauración al terminar

La restauración se hace en `finally`, por lo que ocurre incluso si hay excepciones durante sniffing.

Se envían respuestas ARP legítimas repetidas para:

- víctima ← (IP/MAC reales del gateway)
- gateway ← (IP/MAC reales de la víctima)

Esto es clave en evaluación, porque una salida sin restaurar ARP se considera fallo del comportamiento esperado.

---

## 7) Sniffing FTP y detección de nombres

Se observa solo control FTP (puerto 21), no tráfico cifrado.

Reglas de salida:

- Si línea FTP empieza por `STOR ` → imprime `[FTP][UPLOAD] <nombre>`
- Si línea FTP empieza por `RETR ` → imprime `[FTP][DOWNLOAD] <nombre>`
- Con `-v` también imprime eventos de control (`USER`, `PASS`, `TYPE`, `PASV`, etc.)

Esto cubre el requisito de mostrar archivos subidos/bajados en tiempo real.

---

## 8) Manejo de errores y robustez

- Validación de formato IPv4 (solo versión 4)
- Validación de MAC por regex
- Rechazo de pares origen/objetivo idénticos
- Captura de excepciones en loop de poisoning y parser de paquetes
- Captura global de errores en `main()` con salida controlada
- Señales `SIGINT`/`SIGTERM` para parada limpia

Si el entorno no permite escribir en `/proc/sys/net/ipv4/ip_forward` (caso rootless), el programa no aborta: avisa por warning y continúa.

No hay salida brusca tipo segfault (Python) ni finalización no controlada por errores de entrada.

---

## 9) Entorno de laboratorio

El repo incluye:

- `env/docker-compose.yml`
- Dockerfiles de usuario y nodo atacante
- `Makefile` para levantar/parar sin intervención manual

Comandos rápidos:

```bash
make up
make ps
make logs
make down
```

---

## 10) Limitaciones esperadas (alineadas con subject)

- Solo IPv4
- Solo FTP en claro (control port 21)
- Tráfico cifrado no inspeccionable en esta práctica
- Requiere privilegios de red (`NET_ADMIN`, `NET_RAW` o root)

---

## 11) Recomendaciones para demo estable

- Confirmar IP/MAC por `docker inspect` en cada arranque (pueden cambiar).
- Verificar tablas ARP en contenedores con `cat /proc/net/arp`.
- Ejecutar ataque antes de iniciar acciones FTP.
- Parar siempre con `CTRL+C` para restauración limpia.
