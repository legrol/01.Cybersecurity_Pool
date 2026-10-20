# Comandos para la evaluacion de Stockholm

## 1) Comprobaciones iniciales del repo
```bash
cd /home/rdel-olm/Desktop/stockholm
ls -la
cat README.md
cat Makefile
```

## 2) Preparar entorno de prueba
```bash
mkdir -p "$HOME/infection"
find "$HOME/infection" -mindepth 1 -delete

echo "contenido doc" > "$HOME/infection/a.doc"
echo "contenido jpg" > "$HOME/infection/b.jpg"
echo "no debe tocarse" > "$HOME/infection/ignorado.xyz"
```

## 3) Verificar ayuda y version
```bash
python3 stockholm.py -h
python3 stockholm.py -v
```

## 4) Ejecutar cifrado
```bash
python3 stockholm.py
ls -la "$HOME/infection"
```
Esperado:
- `a.doc` y `b.jpg` pasan a `a.doc.ft` y `b.jpg.ft`.
- `ignorado.xyz` no se cifra.
- Se genera `clave.key` en la raiz del proyecto.

## 5) Comprobar que el archivo cifrado no es legible
```bash
cat "$HOME/infection/a.doc.ft"
```
Esperado:
- Salida no legible para humano (contenido cifrado).

## 6) Guardar la clave y descifrar
```bash
KEY=$(tr -d '\n' < clave.key)
python3 stockholm.py -r "$KEY"
ls -la "$HOME/infection"
cat "$HOME/infection/a.doc"
```
Esperado:
- Se elimina sufijo `.ft`.
- El contenido vuelve a ser legible.

## 7) Probar modo silencioso
```bash
echo "otro doc" > "$HOME/infection/c.doc"
python3 stockholm.py -s
ls -la "$HOME/infection"
KEY=$(tr -d '\n' < clave.key)
python3 stockholm.py -r "$KEY" -s
ls -la "$HOME/infection"
```
Esperado:
- No hay salida de progreso durante ejecucion con `-s`.
- El trabajo se realiza igualmente.

## 8) Probar error de clave invalida (control de errores)
```bash
python3 stockholm.py -r "clave_invalida"
```
Esperado:
- El programa no hace crash.
- Maneja el error y continua controladamente.

## 9) Opcional: limpiar entorno
```bash
make fclean
find "$HOME/infection" -mindepth 1 -delete
```
