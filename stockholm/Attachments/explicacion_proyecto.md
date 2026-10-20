# Explicacion del proyecto Stockholm

## Objetivo
Stockholm es un proyecto educativo para entender como funciona un ransomware de forma controlada y en entorno local Linux.
El programa cifra y descifra archivos solo dentro de `~/infection`.

## Flujo general
1. Lee argumentos CLI con `argparse`.
2. Si se usa `-v/--version`, muestra version y termina.
3. Si se usa `-r/--reverse <clave>`, intenta descifrar archivos `.ft`.
4. Si no hay flags, cifra archivos con extensiones objetivo y anade `.ft`.

## Flags soportadas
- `-h`, `--help`: ayuda.
- `-v`, `--version`: version.
- `-s`, `--silent`: sin salida por pantalla.
- `-r`, `--reverse`: descifrado con clave.

## Restriccion de ruta
La ruta objetivo se define con `Path.home() + "/infection"`.
No opera fuera de esa carpeta.

## Seleccion de archivos
- Cifrado: solo archivos con extensiones asociadas a WannaCry.
- Descifrado: solo archivos que terminan en `.ft`.

## Algoritmo de cifrado y justificacion
Se usa `cryptography.fernet`.
Fernet usa cifrado simetrico autenticado (AES-CBC + HMAC) y es una opcion conocida, robusta y ampliamente usada para practicas seguras.
La clave se genera con `Fernet.generate_key()` y supera el minimo de 16 caracteres exigido.

## Proceso de cifrado
1. Se recorren archivos de `~/infection` (incluyendo subcarpetas).
2. Se filtran por extension valida.
3. Se genera clave y se guarda en `clave.key`.
4. Se cifra contenido en binario.
5. Se sobrescribe archivo y se renombra anadiendo `.ft`.

## Proceso de descifrado
1. Se listan archivos `.ft`.
2. Se usa la clave pasada por `-r` (texto de clave, no ruta).
3. Se descifra cada archivo de forma individual.
4. Se restaura nombre quitando `.ft`.

## Manejo de errores
El programa no usa salidas abruptas por validaciones internas y maneja errores por archivo con `try/except`.
Si un archivo falla, informa del archivo problematico (si no esta en `-s`) y continua con el resto.

## Consideraciones para evaluacion
- Requiere Linux y Python 3.
- Dependencia: `cryptography` (instalable con `make`).
- El README esta limitado a menos de 50 lineas y documenta uso obligatorio.
- El Makefile incluye reglas basicas de instalacion y limpieza.

## Uso responsable
Proyecto exclusivamente educativo.
No debe usarse para fines maliciosos ni fuera de un entorno de pruebas controlado.
