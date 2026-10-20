# Cybersecurity Pool

![Ilustración de la Cybersecurity Pool](zz_Others/cybersecurity-pool.svg)

Colección de proyectos prácticos de ciberseguridad desarrollados en el bootcamp de 42. La pool reúne ejercicios de análisis, criptografía, redes y seguridad web, con documentación y material de evaluación para cada módulo.

> **Uso responsable:** los proyectos son material educativo. Ejecuta las pruebas únicamente en sistemas propios, laboratorios locales o entornos para los que tengas autorización explícita. En particular, `inquisitor` y `vaccine` pueden generar tráfico de prueba y `stockholm` cifra archivos.

## Proyectos

| Proyecto | Área | Qué encontrarás |
| --- | --- | --- |
| [Arachnida](Arachnida/README.md) | Análisis web y metadatos | `spider.py` recopila imágenes de páginas web y `scorpion.py` inspecciona sus metadatos. |
| [ft_otp](ft_otp/README.md) | Criptografía y autenticación | Generación de códigos OTP temporales a partir de una clave hexadecimal. |
| [ft_onion](ft_onion/README.md) | Redes y privacidad | Servicio web oculto en Tor, con Nginx y acceso SSH en un entorno configurable. |
| [Inquisitor](inquisitor/README.md) | Redes y análisis de tráfico | Laboratorio de ARP poisoning y observación de nombres de archivos en tráfico FTP. |
| [Reverse](reverse/README.md) | Ingeniería inversa | Análisis de binarios y reconstrucción de la lógica de varios niveles. |
| [Stockholm](stockholm/README.md) | Criptografía y malware | Simulación educativa de cifrado y recuperación de archivos en una carpeta de prueba. |
| [Vaccine](vaccine/README.md) | Seguridad web | Pruebas de SQL injection, con servidor local de demostración incluido. |

## Cómo empezar

Cada proyecto tiene sus propios requisitos y pasos de ejecución. Entra en la carpeta que te interese y sigue su README; no hay una instalación única para toda la pool.

```bash
cd Arachnida
```

Varios proyectos incluyen guías adicionales, comandos de evaluación o laboratorios Docker. Consulta la documentación del módulo antes de ejecutar herramientas o preparar un entorno.

## Estructura

```text
.
├── Arachnida/
├── ft_otp/
├── ft_onion/
├── inquisitor/
├── reverse/
├── stockholm/
├── vaccine/
├── zz_Others/
├── zz_Subjects _Cyber/
└── zz_Subject_Corrections/
```

Las carpetas `zz_Subjects _Cyber` y `zz_Subject_Corrections` contienen subjects y correcciones de referencia.

## Tecnologías y conceptos

Python · C · Linux · Docker · Tor · Nginx · SSH · OTP · análisis de tráfico · ingeniería inversa · seguridad web.

---

Proyecto personal de aprendizaje realizado en el contexto de la Cybersecurity Pool de 42.