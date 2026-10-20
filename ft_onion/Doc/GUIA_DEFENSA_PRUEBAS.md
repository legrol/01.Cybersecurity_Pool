# FT_ONION - Guía Completa: Pruebas y Defensa

## PARTE 1: VALIDACIÓN (PRUEBAS)

Elige tu entorno y sigue los pasos.

---

## 🐳 OPCIÓN A: Docker (42 sin sudo)

### A.1 - Verificar que el container está corriendo

```bash
docker ps | grep ft_onion
docker compose ps
```

**Esperado:** Estado "running", puertos correctos (8080:80, 2222:4242).

### A.2 - Ver logs de servicios

```bash
docker compose logs ft_onion | head -20
```

**Esperado:** Sin errores, mensaje "Successfully started" o similar.

### A.3 - Probar Nginx local

```bash
curl -I http://127.0.0.1:8080
curl http://127.0.0.1:8080 | head -10
```

**Esperado:** 
```
HTTP/1.1 200 OK
...
<h1>Servidor Onion Activo</h1>
```

### A.4 - Probar SSH

```bash
docker exec <container_id> ss -ltnp | grep 4242
```

**Esperado:** `sshd` escuchando en `127.0.0.1:4242`.

O acceso directo:
```bash
ssh -p 2222 evaluator@127.0.0.1
# password: evaluator42
exit
```

### A.5 - Obtener dirección .onion

```bash
docker compose logs | grep -i onion
```

O:
```bash
docker exec <container_id> cat /var/lib/tor/onion_web_service/hostname
```

**Esperado:** Dirección tipo `xxxxxxxxxxxxxxxxxxxxxxxx.onion`

### A.6 - Prueba en Tor Browser

1. Abre **Tor Browser** y conecta.
2. Navega a: `http://<tu_onion>`
3. Deberías ver "Servidor Onion Activo".

**Si no carga:** Espera 30-60 segundos, Tor tarda en propagar.

---

## 🐧 OPCIÓN B: Sistema local con sudo

### B.1 - Validar sintaxis

```bash
sudo nginx -t
sudo sshd -t -f /etc/ssh/sshd_config
sudo tor --verify-config -f /etc/tor/torrc
```

**Esperado:** Todos sin errores.

### B.2 - Verificar estado de servicios

```bash
sudo systemctl status nginx --no-pager | grep Active
sudo systemctl status ssh --no-pager | grep Active
sudo systemctl status tor --no-pager | grep Active
```

**Esperado:** Los tres en "active (running)".

### B.3 - Probar Nginx local

```bash
curl -I http://127.0.0.1:80
curl http://127.0.0.1:80 | head -10
```

**Esperado:**
```
HTTP/1.1 200 OK
...
<h1>Servidor Onion Activo</h1>
```

### B.4 - Probar SSH

```bash
sudo ss -ltnp | grep 4242
```

**Esperado:** `sshd` escuchando en `0.0.0.0:4242` o `127.0.0.1:4242`.

### B.5 - Obtener dirección .onion

```bash
sudo cat /var/lib/tor/onion_web_service/hostname
```

**Esperado:** Dirección tipo `xxxxxxxxxxxxxxxxxxxxxxxx.onion`

### B.6 - Prueba en Tor Browser

1. Abre **Tor Browser** y conecta.
2. Navega a: `http://<tu_onion>`
3. Deberías ver "Servidor Onion Activo".

---

## Diagnóstico rápido

| Problema | Solución |
|----------|----------|
| Container no inicia | `docker-compose logs` → revisar errores |
| Nginx no responde | `curl http://127.0.0.1:8080` (Docker) o `sudo systemctl restart nginx` |
| SSH no aparece | `docker exec <id> ss -ltnp \| grep 4242` o `sudo ss -ltnp \| grep 4242` |
| .onion no carga en navegador | Esperar 30-60 seg, Tor propaga lentamente |
| Puerto ocupado (sistema local) | Cambiar a Docker o VM con mapeo |

---

---

# PARTE 2: DEFENSA EN EVALUACIÓN

Tiempo total: 5-10 minutos.

---

## 📝 PASO 1: Introducción (30 segundos)

Dices esto:

> "En este proyecto publico una página web estática en la red Tor,
> utilizando un hidden service.
>
> La arquitectura es simple:
> - Nginx sirve la página en puerto 80 (interno)
> - SSH escucha en puerto 4242 (interno)
> - Tor crea un hidden service (.onion) que publica ambos servicios
>
> Cumplo exactamente lo que pide el subject: página estática, Nginx obligatorio,
> HTTP 80, SSH 4242, hidden service Tor, sin cambios de puertos ni firewall."

---

## 🐳 PASO 2A: Demo Docker (si usas Docker)

### Demo paso a paso

```bash
# 1. Mostrar que container está corriendo
docker ps | grep ft_onion
```

**Dices:**
> "El container está corriendo con port mapping: 8080 hacia puerto 80 (Nginx) y 
> 2222 hacia puerto 4242 (SSH) internamente."

```bash
# 2. Probar web local
curl -I http://127.0.0.1:8080
```

**Dices:**
> "Nginx responde correctamente en puerto 80 (mapeado a 8080 desde afuera)."

```bash
# 3. Verificar SSH
docker exec <container_id> ss -ltnp | grep 4242
```

**Dices:**
> "SSH escucha en puerto 4242 internamente, como exige Tor."

```bash
# 4. Obtener .onion
docker-compose logs | grep -i onion
# O:
docker exec <container_id> cat /var/lib/tor/onion_web_service/hostname
```

**Dices:**
> "Tor ha generado la dirección .onion que identifica este hidden service."

---

## 🐧 PASO 2B: Demo Sistema local con sudo

### Demo paso a paso

```bash
# 1. Validar configs
sudo nginx -t
sudo sshd -t -f /etc/ssh/sshd_config
sudo tor --verify-config -f /etc/tor/torrc
```

**Dices:**
> "Todas las configuraciones son válidas y coherentes."

```bash
# 2. Verificar servicios
sudo systemctl status nginx --no-pager | grep Active
sudo systemctl status ssh --no-pager | grep Active
sudo systemctl status tor --no-pager | grep Active
```

**Dices:**
> "Los tres servicios están activos."

```bash
# 3. Probar web local
curl -I http://127.0.0.1:80
```

**Dices:**
> "Nginx responde correctamente en puerto 80."

```bash
# 4. Verificar SSH
sudo ss -ltnp | grep 4242
```

**Dices:**
> "SSH escucha en puerto 4242, como se requiere."

```bash
# 5. Obtener .onion
sudo cat /var/lib/tor/onion_web_service/hostname
```

**Dices:**
> "Tor ha generado el hidden service .onion."

---

## 🌐 PASO 3: Abrir en Tor Browser (2-3 minutos)

```bash
# Copiar tu .onion
# (copiaste la dirección anterior)
```

1. Abre **Tor Browser**
2. Verifica que está conectado a Tor (debería estar verde)
3. Navega a: `http://<tu_onion>`
4. La página debería cargar

**Dices mientras carga:**
> "Accedo a través de Tor Browser. Tor redirige el tráfico a mi hidden service.
> La página debería cargar en 2-3 segundos."

**Cuando los ve:**
> "La página caraga correctamente a través de la dirección .onion.
> Esto demuestra que:
> 1. Nginx está sirviendo index.html en puerto 80
> 2. Tor redirige el tráfico .onion:80 a localhost:80
> 3. El hidden service funciona correctamente"

---

## ❓ PASO 4: Preguntas frecuentes (varían)

### P: ¿Quién sirve la página?

**R:**
> "Nginx. Tor solo publica el .onion y redirecciona el tráfico.
> El servidor web que el usuario ve en el navegador es Nginx respondiendo
> en localhost:80."

---

### P: ¿Dónde está SSH?

**R:**

**Opción A - Con torsocks (si lo tienes):**
```bash
torsocks ssh -p 4242 usuario@<tu_onion>
```

**R:**
> "SSH es accesible en puerto 4242 y está publicado por el hidden service.
> Puede conectársele a través de la dirección .onion en puerto 4242."

**Opción B - Solo validación (sin torsocks):**
```bash
# Docker:
docker exec <id> ss -ltnp | grep 4242

# Sistema local:
sudo ss -ltnp | grep 4242

# Verificar torrc:
grep "HiddenServicePort 4242" /etc/tor/torrc
```

**R:**
> "SSH escucha en puerto 4242 (como ves aquí) y está publicado en el 
> hidden service por Tor. La validación mínima es que el puerto está 
> configurado correctamente."

---

### P: ¿Abriste puertos en el router?

**R:**
> "No. El subject pide no abrir puertos ni reglas de firewall.
> Los servicios están expuestos solo a través de Tor, que actúa como 
> intermediario seguro."

---

### P: ¿Hay backend, framework o base de datos?

**R:**
> "No. Solo una página HTML estática pura, servida por Nginx.
> Sin backend, sin base de datos, sin framework.
> Exactamente como pide el subject."

---

### P: ¿Por qué dockerfile? ¿No tenías sudo?

**R:**
> "Exacto. En 42 no tengo permisos sudo. Docker me permite ejecutar
> servicios en un container sin privilegios elevados.
> 
> Internamente el container sigue usando puertos 80 y 4242 (como exige Tor).
> Desde afuera accedo por 8080 y 2222 (port mapping).
>
> Funcionalmente es idéntico al project en una máquina normal."

---

### P: ¿Y si el puerto 4242 estuviera ocupado en tu máquina?

**R:**
> "Usaría una VM o Docker con port mapping, como en este caso.
> Los puertos internos deben seguir siendo 80 y 4242 (Tor lo requiere).
> El mapeo externo no afecta al funcionamiento de Tor."

---

## 🏁 PASO 5: Cierre (20 segundos)

> "En resumen:
> - Página estática en index.html: ✓
> - Nginx en puerto 80: ✓
> - SSH en puerto 4242: ✓
> - Hidden service Tor (.onion): ✓
> - Accesible a través de Tor Browser: ✓
>
> Solución mínima funcional que cumple exactamente el subject.
> Sin extras, sin complejidad innecesaria."

---

## ☑️ Checklist Final

Antes de defender, verifica:

- [ ] Container está corriendo (Docker) O servicios activos (sudo)
- [ ] Nginx responde: `curl http://127.0.0.1:80` (local) o `http://127.0.0.1:8080` (Docker)
- [ ] SSH escucha en 4242: `ss -ltnp | grep 4242`
- [ ] Dirección .onion obtenida
- [ ] Tor Browser abierto y conectado
- [ ] .onion carga correctamente
- [ ] Memoricé el guion de 30 segundos
- [ ] Sé responder las 6 preguntas frecuentes

---

## 💡 Último consejo

El proyecto es correcto. La defensa es solo **demostrar que funciona**.

Ejecuta los comandos en orden, muestra que responden, abre .onion en Tor Browser.

Eso es todo. 💪
