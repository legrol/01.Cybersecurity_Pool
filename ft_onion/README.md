# ft_onion - Hidden Service Tor con Nginx y SSH

Publica una página web estática en la red Tor usando un hidden service.

**Requisitos:** Página HTML única • Nginx puerto 80 • SSH puerto 4242 • Hidden service .onion • Sin puertos extra • Sin firewall

---

## 🚀 Instalación rápida (3 minutos)

### Para 42 sin sudo (Docker - RECOMENDADO):

```bash
cd /ruta/a/ft_onion
docker build -t ft_onion .
docker compose up -d
docker compose logs | grep -i onion  # Tu dirección .onion
```

### Para máquina local con sudo:

```bash
sudo cp index.html /var/www/html/index.html
sudo cp nginx.conf /etc/nginx/nginx.conf
sudo cp sshd_config /etc/ssh/sshd_config
sudo cp torrc /etc/tor/torrc
sudo systemctl restart nginx ssh tor
sudo cat /var/lib/tor/onion_web_service/hostname  # Tu .onion
```

---

## ✓ Validación rápida

**Docker:**
```bash
curl http://127.0.0.1:8080          # Nginx responde
docker exec <id> ss -ltnp | grep 4242  # SSH en 4242
docker-compose logs | grep "Dirección"  # .onion
```

**Sistema local:**
```bash
curl http://127.0.0.1:80             # Nginx responde
sudo ss -ltnp | grep 4242            # SSH en 4242
sudo cat /var/lib/tor/onion_web_service/hostname  # .onion
```

---

## 🌐 En Tor Browser

1. Abre Tor Browser y conecta a Tor
2. Navega a: `http://<tu_direccion_onion>`
3. Deberías ver "Servidor Onion Activo"

---

## 📁 Archivos

| Archivo | Propósito |
|---------|-----------|
| `index.html` | Página estática |
| `nginx.conf` | Nginx puerto 80 |
| `sshd_config` | SSH puerto 4242 |
| `torrc` | Hidden service Tor |
| `Dockerfile` | Image container (42) |
| `docker-compose.yml` | Orquestación (42) |

---

## 📚 Documentación (4 documentos)

Elige según tu necesidad:

| Necesito | Archivo |
|----------|---------|
| Instalar en 42 sin sudo | [DOCKER_42.md](Doc/DOCKER_42.md) |
| Validar que funciona | [GUIA_DEFENSA_PRUEBAS.md](Doc/GUIA_DEFENSA_PRUEBAS.md) (Parte 1) |
| Defender en evaluación | [GUIA_DEFENSA_PRUEBAS.md](Doc/GUIA_DEFENSA_PRUEBAS.md) (Parte 2) |
| Memorizar lo esencial | [Attachments/CHULETA_COMPACTA.txt](Attachments/CHULETA_COMPACTA.txt) |

**Recomendado:** Lee README (aquí) → DOCKER_42.md si necesario → GUIA_DEFENSA_PRUEBAS.md → CHULETA_COMPACTA.txt

---

## 🔧 Comandos útiles (Docker)

```bash
docker-compose logs -f              # Ver logs en vivo
docker exec -it <id> bash           # Entrar al container
docker-compose down                 # Parar
docker-compose up -d --build        # Rebuild
docker ps                            # Ver estado
```

---

## Port mapping (Docker)

```
Tu máquina 42    →    Container
8080             →    80 (Nginx)
2222             →    4242 (SSH)

Tor ve internamente: localhost:80 y localhost:4242 ✓
```

---

## Cumplimiento del subject

✓ Página estática única (index.html)
✓ Nginx servidor web obligatorio
✓ HTTP puerto 80 (interno)
✓ SSH puerto 4242 (interno)
✓ Hidden service Tor (.onion)
✓ Sin puertos extra • Sin firewall
✓ Sin sudo necesario (Docker)
✓ Configuración mínima
