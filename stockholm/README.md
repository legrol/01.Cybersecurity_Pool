# Stockholm

Proyecto educativo de ciberseguridad para comprender el funcionamiento del ransomware (WannaCry).
**Solo para fines educativos. Nunca usar de manera maliciosa.**

## Requisitos y Configuración
- Sistema operativo: **Linux**.
- Python 3 y la librería `cryptography`.

Para instalar las dependencias requeridas mediante el `Makefile` incluido en la raíz de este proyecto:
```bash
make
```

## Instrucciones de Uso
El programa cifra y descifra únicamente los archivos compatibles ubicados en la carpeta obligatoria `~/infection` (en el directorio $HOME del usuario actual).

### Parámetros Disponibles:
- `-h`, `--help`    : Muestra la información de ayuda y describe los parámetros.
- `-v`, `--version` : Muestra la versión actual del programa por consola.
- `-s`, `--silent`  : Activa el modo sigiloso. No muestra salida por pantalla de los archivos cifrados/descifrados.
- `-r`, `--reverse` : Descifra los archivos revirtiendo la infección. Requiere la clave de cifrado generada previamente indicada por argumentos de terminal.

### 1. Infección (Cifrar)
Ejecuta el programa sin argumentos para infectar (cifrar) los archivos en la ruta `~/infection`.
Renombrará los archivos añadiendo la extensión `.ft` y generará una clave local llamada `clave.key`.
```bash
python3 stockholm.py
```

### 2. Recuperación (Descifrar)
Utiliza la clave secreta proporcionada en el flag `-r` o `--reverse`. Nunca pases la ruta del archivo, pasa su contenido.
```bash
python3 stockholm.py --reverse "TU_CLAVE_AQUI"
```

## Comportamiento esperado
- Solo actúa en `~/infection`.
- Solo cifra extensiones incluidas en el listado objetivo de WannaCry.
- Renombra archivos cifrados añadiendo `.ft`.
- Ignora archivos que ya terminan en `.ft` durante el cifrado.
- En descifrado, procesa archivos `.ft` y restaura su nombre original.
