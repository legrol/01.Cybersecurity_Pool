# Reverse Passion

Proyecto de **reverse engineering** orientado a evaluación y estudio, con resolución de los niveles obligatorios:
- `level1` (resuelto)
- `level2` (resuelto)
- `level3` (incluido como extra, no obligatorio)

## Objetivo

Recrear en C la lógica de binarios tipo crackme y validar su comportamiento.

Este repositorio incluye:
- Passwords válidas para `level1` y `level2`.
- Implementaciones en C (`source.c`) de ambos niveles.
- Binarios originales en `binary/`.
- Documentación y material técnico en `Attachments/`.

## Estructura del proyecto

```text
reverse/
├─ level1/
│  ├─ password
│  └─ source.c
├─ level2/
│  ├─ password
│  └─ source.c
├─ binary/
│  ├─ level1
│  ├─ level2
│  └─ level3
├─ Attachments/
│  ├─ [Estudio]
│  ├─ ENTORNO_LINUX.md
│  ├─ INICIO.md
│  ├─ INDICE_ESTUDIO.md
│  ├─ RESUMEN_VISUAL.md
│  ├─ TUTORIAL_LEVEL1.md
│  ├─ TUTORIAL_LEVEL2.md
│  ├─ HERRAMIENTAS_REFERENCIA.md
│  ├─ my_guide
│  ├─ [Artefactos técnicos]
│  ├─ level1_strings.txt
│  ├─ level1_disassembly.txt
│  ├─ level2_strings.txt
│  ├─ level2_disassembly.txt
│  ├─ level3_strings.txt
│  └─ level3_disassembly.txt
```

## Documentación

Ruta recomendada para estudiar el proyecto:
1. `Attachments/INICIO.md`
2. `Attachments/RESUMEN_VISUAL.md`
3. `Attachments/TUTORIAL_LEVEL1.md`
4. `Attachments/TUTORIAL_LEVEL2.md`
5. `Attachments/HERRAMIENTAS_REFERENCIA.md`
6. `Attachments/INDICE_ESTUDIO.md`

## Artefactos técnicos

Archivos de evidencia generados del análisis estático:
- `Attachments/level1_strings.txt`
- `Attachments/level1_disassembly.txt`
- `Attachments/level2_strings.txt`
- `Attachments/level2_disassembly.txt`
- `Attachments/level3_strings.txt`
- `Attachments/level3_disassembly.txt`
- `Attachments/my_guide` (chuleta rápida de comandos)

## Requisitos

- Linux (VM o máquina Linux)
- `gcc`
- Recomendado para análisis: `binutils` (`strings`, `objdump`) y `gdb`

## Compilación

Desde la raíz del proyecto:

```bash
gcc -Wall -Wextra -Werror level1/source.c -o level1/source.out
gcc -Wall -Wextra -Werror level2/source.c -o level2/source.out
```

## Ejecución y validación

### Level 1

```bash
cat level1/password
printf "$(cat level1/password)\n" | ./level1/source.out
```

Resultado esperado: `Good job.`

Password entregada:

```text
__stack_check
```

### Level 2

```bash
cat level2/password
printf "$(cat level2/password)\n" | ./level2/source.out
```

Resultado esperado: `Good job.`

Password entregada:

```text
00101108097098101114101
```

## Resumen técnico

- **level1**: compara el input directamente contra una cadena fija.
- **level2**: valida prefijo `00`, decodifica bloques de 3 dígitos a ASCII y compara contra `delabere`.

## Nota

La entrega cubre el mínimo obligatorio del subject (niveles 1 y 2).
