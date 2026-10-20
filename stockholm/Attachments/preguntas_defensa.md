# Preguntas y respuestas para la defensa de Stockholm

## 1) Que hace exactamente tu programa
Cifra y descifra archivos en un entorno local controlado, solo dentro de `~/infection`, con fines educativos para entender el comportamiento de un ransomware.

## 2) Que flags soporta
- `-h` / `--help`
- `-v` / `--version`
- `-s` / `--silent`
- `-r` / `--reverse <clave>`

## 3) Donde actua el programa
Solo en la carpeta `~/infection` del usuario actual, usando `Path.home()`.

## 4) Que archivos cifra
Solo los que coinciden con extensiones del listado objetivo inspirado en WannaCry.

## 5) Como marca un archivo cifrado
Renombra el archivo añadiendo la extension `.ft`.

## 6) Como revierte la infeccion
Con `-r <clave>`: busca archivos `.ft`, descifra su contenido y restaura el nombre original quitando `.ft`.

## 7) Que algoritmo usas y por que
Uso `cryptography.fernet`, que ofrece cifrado simetrico autenticado con primitivas criptograficas estandar y una API segura para este proyecto educativo.

## 8) La clave cumple el requisito del subject
Si. Se genera con `Fernet.generate_key()` y supera claramente el minimo de 16 caracteres.

## 9) Que pasa si la clave es invalida
No hay crash. El programa informa del error de formato y termina de forma controlada.

## 10) Que pasa si un archivo no se puede descifrar
Se reporta el archivo que falla y el programa continua con el resto.

## 11) Como demuestras que el cifrado es real
Antes del cifrado el contenido es legible; despues de cifrar no es legible y el nombre termina en `.ft`.

## 12) Como demuestras que el descifrado funciona
Tras descifrar con la clave correcta, desaparece `.ft` y el contenido vuelve a ser legible.

## 13) Tienes manejo de errores
Si. Se manejan errores por archivo y tambien errores de clave sin detener el programa de forma inesperada.

## 14) README y Makefile cumplen
Si. Ambos existen en la raiz, no estan vacios, y el README esta por debajo de 50 lineas.

## 15) Uso etico
Es un proyecto exclusivamente educativo en entorno controlado. No se debe usar con fines maliciosos.
