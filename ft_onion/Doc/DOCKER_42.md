# Docker en 42 - Solución sin sudo

## Problema en 42

- ❌ Sin permisos `sudo`
- ❌ Puerto 4242 ocupado (servicios del sistema)
- ✓ Solución: **Docker con port mapping**

---

## Requisitos

```bash
docker --version
docker-compose --version
```

Si no están instalados, pídele a un admin o usa una **VM local** en tu máquina.

---

## Instalación (3 pasos, 3 minutos)

### Paso 1: Construir imagen

```bash
cd /ruta/a/ft_onion
docker build -t ft_onion .
```

Espera ~2 minutos. **Esperado:** `Successfully tagged ft_onion:latest`

### Paso 2: Levantar container

```bash
docker-compose up -d
```

Espera 3-5 segundos.

### Paso 3: Obtener .onion

```bash
docker-compose logs | grep -i onion
```

O:
```bash
docker exec <container_id> cat /var/lib/tor/onion_web_service/hostname
```

**Esperado:** Dirección `xxxxxxxxxxxxxxxxxxxxxxxx.onion`

---

## ¿Por qué funciona esto?

```
Tu máquina 42 (EXTERNO)    →    Container (INTERNO)
─────────────────────────────────────────────────────
Puerto 8080 (curl aquí)    →    Puerto 80 (Nginx)
Puerto 2222 (ssh aquí)     →    Puerto 4242 (SSH)

Tor DENTRO del container ve:
  - localhost:80 (Nginx)
  - localhost:4242 (SSH)
  
Result: .onion funciona correctamente ✓
```

---

## Verificación rápida

```bash
# ¿Container está corriendo?
docker ps | grep ft_onion

# ¿Nginx responde?
curl -I http://127.0.0.1:8080

# ¿SSH escucha internamente?
docker exec <id> ss -ltnp | grep 4242

# ¿.onion existe?
docker exec <id> cat /var/lib/tor/onion_web_service/hostname
```

---

## En Tor Browser

1. Abre **Tor Browser**
2. Conecta a Tor
3. Navega a: `http://<tu_onion>`
4. Ves "Servidor Onion Activo" ✓

---

## Acceso desde 42

```bash
# Web (puerto mapeado a 8080)
curl http://127.0.0.1:8080

# SSH (puerto mapeado a 2222)
ssh -p 2222 evaluator@127.0.0.1
# password: evaluator42
```

---

## Comandos útiles

```bash
# Logs en vivo
docker-compose logs -f

# Entrar al container
docker exec -it <container_id> bash

# Ver estado
docker ps
docker-compose ps

# Parar servicios
docker-compose down

# Reiniciar con rebuild
docker-compose down
docker-compose up -d --build

# Ver .onion
docker exec <id> cat /var/lib/tor/onion_web_service/hostname

# SSH interno
docker exec <id> ss -ltnp | grep 4242

# Tor status
docker exec <id> systemctl status tor
```

---

## Si algo falla

### Docker no construye

```bash
# Espacio bajo?
docker system prune -a --volumes -f

# Verifica Docker
docker --version
docker ps
```

### Container no inicia

```bash
docker-compose logs
# Revisar output

# Reintentar
docker-compose down
docker-compose up -d
```

### .onion no aparece

```bash
# Tor tarda a veces 30+ segundos
sleep 30
docker exec <id> cat /var/lib/tor/onion_web_service/hostname

# Ver logs de tor
docker exec <id> tail -20 /var/log/tor/log
```

### Nginx no responde

```bash
docker-compose logs | grep nginx
curl http://127.0.0.1:8080

# Restart
docker-compose restart
```

### SSH no conecta

```bash
docker exec <id> ss -ltnp | grep 4242
docker-compose logs | grep ssh

# Restart
docker-compose down
docker-compose up -d
```

---

## Explicación en evaluación

> "No tengo permisos sudo en 42, así que uso Docker.
>
> El container internamente:
> - Nginx en puerto 80
> - SSH en puerto 4242
> - Tor genera .onion
>
> Port mapping desde 42:
> - 8080:80 (acceso local a Nginx)
> - 2222:4242 (acceso local a SSH)
>
> Tor siempre ve los puertos correctos internamente (80 y 4242).
> Funciona exactamente como en una máquina normal."

Luego muestra:
```bash
curl http://127.0.0.1:8080
docker exec <id> cat /var/lib/tor/onion_web_service/hostname
```

Y abre en Tor Browser → **Listo.**

---

## Alternativas si no tienes Docker

### Opción A: Pedir a admin
Solicita que instalen Docker en 42.

### Opción B: VM local
```
Tu máquina 42
     ↓
[VirtualBox/KVM]
     ↓
Ubuntu + Docker
     ↓
docker-compose up
```

Port mapping en VirtualBox: 8080→VM:80, 2222→VM:4242

### Opción C: Otra máquina de 42
Usa una máquina que sí tenga Docker instalado.

---

## Resumen

✓ Sin sudo → Docker
✓ Puerto 4242 ocupado → Port mapping (8080→80, 2222→4242)
✓ Tor ve puertos correctos internamente
✓ Resultado final: .onion funciona perfectamente
✓ Defensa: mismos comandos que en máquina normal

**Docker es la solución perfecta para 42.**
