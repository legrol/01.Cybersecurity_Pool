# Explicacion funcion por funcion de stockholm.py

## Vision general
El script implementa dos flujos:
1. Cifrado de archivos objetivo en `~/infection`.
2. Descifrado de archivos `.ft` usando la clave pasada por `-r`.

Tambien ofrece flags de ayuda, version y modo silencioso.

## Variables globales

### `infectorio`
Ruta de trabajo fija: `Path.home() + "/infection"`.
Con esto se cumple el requisito del subject de actuar solo en la carpeta `infection` del HOME.

### `ver_sem`
Cadena de version que se imprime cuando se usa `-v`.

### `extensiones`
Lista de extensiones objetivo para el modo cifrado.
Solo los archivos que terminen en alguna de estas extensiones se cifran.

## `leer_argumentos()`
Responsabilidad:
- Llamar al parser y devolver los valores de los flags relevantes.

Que devuelve:
- `r`: clave para descifrado (o `None`).
- `v`: booleano para version.
- `s`: booleano para modo silencioso.

## `inicializar_analizador()`
Responsabilidad:
- Configurar `argparse`.
- Definir flags soportadas.

Flags definidas:
- `-r` / `--reverse` con argumento `clave`.
- `-v` / `--version`.
- `-s` / `--silent`.

Devuelve el resultado de `parse_args()`.

## `validar_fichero(elemento, modo)`
Responsabilidad:
- Decidir si un archivo debe procesarse.

Reglas:
- Debe ser archivo real (`os.path.isfile`).
- Excluye `stockholm.py` y `clave.key`.
- Si `modo == "c"`: valida por extension objetivo.
- Si `modo == "d"`: valida que termine en `.ft`.

Salida:
- `True` si es valido para el modo.
- `False` en cualquier otro caso.

## `contenido(carpeta)`
Responsabilidad:
- Recorrer recursivamente una carpeta y devolver todos los archivos encontrados.

Comportamiento:
- Si `carpeta` existe y es directorio, lista su contenido.
- Si encuentra subdirectorios, se llama recursivamente.
- Si la carpeta no existe o no es directorio, informa (si no hay `-s`) y devuelve lista vacia.

Salida:
- Lista de rutas completas de archivos.

## `secuestrar()`
Responsabilidad:
- Cifrar archivos objetivo y renombrarlos con `.ft`.

Flujo:
1. Obtiene todos los archivos de `infectorio` con `contenido()`.
2. Filtra solo los validos para cifrado con `validar_fichero(..., "c")`.
3. Si no hay candidatos, informa y termina sin regenerar clave.
4. Genera clave con `Fernet.generate_key()`.
5. Guarda la clave en `clave.key`.
6. Para cada archivo valido:
   - lee bytes,
   - cifra,
   - sobrescribe,
   - renombra a `nombre_original + ".ft"`.
7. Muestra resumen final (si no hay `-s`).

Salida:
- Numero de archivos cifrados con exito.

## `liberar(clave)`
Responsabilidad:
- Descifrar archivos `.ft` con la clave recibida por parametro.

Flujo:
1. Busca archivos `.ft` en `infectorio`.
2. Muestra lista de cifrados (si no hay `-s`).
3. Convierte `clave` a bytes si viene como string.
4. Valida formato de clave creando instancia `Fernet(clave)`.
5. Recorre cada `.ft`:
   - lee bytes,
   - descifra,
   - sobrescribe,
   - renombra quitando los 3 ultimos caracteres (`.ft`).
6. Maneja errores por archivo:
   - `InvalidToken`: clave incorrecta o token invalido.
   - excepcion general: fallo de lectura/escritura/renombrado.
7. Muestra resumen final de descifrados (si no hay `-s`).

Salida:
- Numero de archivos descifrados con exito.

## Bloque principal `if __name__ == "__main__":`
Responsabilidad:
- Elegir flujo segun argumentos.

Decision:
1. Si `-v`: imprime version.
2. Si `-r`: llama a `liberar(revertir)`.
3. Si no hay flags: intenta cifrar con `secuestrar()` si existe `infectorio`.
4. Si no existe `infectorio`: informa error (si no hay `-s`).

## Resumen de comportamiento esperado
- El cifrado solo afecta extensiones objetivo en `~/infection`.
- Cada archivo cifrado se marca con `.ft`.
- El descifrado requiere clave valida pasada por terminal.
- El programa evita paradas abruptas en validaciones internas y reporta errores de forma controlada.
