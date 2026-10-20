# RESUMEN VISUAL: Proyecto Reverse Passion

## OBJETIVO DEL PROYECTO

```
┌──────────────────────────────────────────────────────┐
│                REVERSE PASSION PROJECT              │
│                                                      │
│  Objetivo: Reverse Engineer 2-3 binarios             │
│  Dificultad: Fácil → Difícil                        │
│  Herramientas: gdb, objdump, strings, etc.          │
│  Entrega: source.c + password para cada nivel      │
└──────────────────────────────────────────────────────┘
```

---

## ESTRUCTURA DEL PROYECTO

```
/home/rdel-olm/Desktop/reverse/
│
├── binary/
│   ├── level1              (ELF 32-bit ejecutable)
│   ├── level2              (ELF 32-bit ejecutable)
│   └── level3              (Extra, no obligatorio)
│
├── level1/                 ✅ OBLIGATORIO
│   ├── password            ("__stack_check")
│   └── source.c            (Código C recreado)
│
├── level2/                 ✅ OBLIGATORIO
│   ├── password            ("00101108097098101114101")
│   └── source.c            (Código C recreado)
│
├── Attachments/
│   ├── EXPLICACION.md      (Descripción del proyecto)
│   ├── ENTORNO_LINUX.md    (Guía del entorno)
│   └── ...
│
├── TUTORIAL_LEVEL1.md      (Guía paso a paso nivel fácil)
├── TUTORIAL_LEVEL2.md      (Guía paso a paso nivel intermedio)
├── HERRAMIENTAS_REFERENCIA.md  (Referencia de comandos)
│
├── level1_disassembly.txt  (Análisis objdump)
├── level1_strings.txt      (Strings extraídos)
├── level2_disassembly.txt  (Análisis objdump)
└── level2_strings.txt      (Strings extraídos)
```

---

## COMPARATIVA: LEVEL1 vs LEVEL2

```
┌─────────────────────────────────────────────────────────────────┐
│                       LEVEL 1                                   │
├─────────────────────────────────────────────────────────────────┤
│ Dificultad: ⭐ (Principiante)                                   │
│ Tipo: Comparación simple                                       │
│ Password: __stack_check                                        │
│                                                                │
│ LÓGICA:                                                        │
│ ┌─────────────────────────────────────────────────────────┐   │
│ │ 1. Leer input                                           │   │
│ │ 2. Comparar: input == "__stack_check"                 │   │
│ │ 3. Si coincide → "Good job." / Si no → "Nope."        │   │
│ └─────────────────────────────────────────────────────────┘   │
│                                                                │
│ DATOS INTERESANTES:                                           │
│ • Buffer: 108 caracteres                                      │
│ • Funciones: printf, scanf, strcmp                            │
│ • Constante visible en strings: "__stack_check"               │
│                                                                │
│ CÓMO OBTENER PASSWORD:                                        │
│ $ strings binary/level1 | grep "stack"                        │
│ __stack_check                                                 │
│                                                                │
│ VALIDACIÓN:                                                   │
│ $ printf "__stack_check\n" | ./binary/level1                  │
│ Please enter key: Good job.  ✓                                │
└─────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────┐
│                       LEVEL 2                                   │
├─────────────────────────────────────────────────────────────────┤
│ Dificultad: ⭐⭐⭐ (Intermedio/Avanzado)                        │
│ Tipo: Algoritmo de decodificación                             │
│ Password: 00101108097098101114101                             │
│                                                                │
│ LÓGICA:                                                        │
│ ┌─────────────────────────────────────────────────────────┐   │
│ │ 1. Validar que empiece con "00"                        │   │
│ │ 2. Leer bloques de 3 dígitos                           │   │
│ │ 3. Convertir cada bloque a número ASCII                │   │
│ │ 4. Construir cadena: out[0]='d' + caracteres          │   │
│ │ 5. Comparar con "delabere"                            │   │
│ │ 6. Si coincide → "Good job." / Si no → "Nope."        │   │
│ └─────────────────────────────────────────────────────────┘   │
│                                                                │
│ DATOS INTERESANTES:                                           │
│ • Buffer input: 24 caracteres (23 + null terminator)         │
│ • Buffer output: 9 caracteres ("delabere" + null)            │
│ • Funciones: printf, scanf, atoi, strcmp, strlen, memset     │
│ • Conversión: ASCII desimal → Carácter                       │
│                                                                │
│ DECODIFICACIÓN:                                               │
│ "00101108097098101114101" → [ 00 | 101 | 108 | 097 | ... ]  │
│ [01 - Validar] [101→'e'] [108→'l'] [097→'a'] [098→'b'] ...  │
│ Resultado: 'd' + "elabere" = "delabere"                      │
│                                                                │
│ TABLA ASCII IMPORTANTE:                                       │
│ a=97   b=98   d=100  e=101  l=108  r=114                     │
│                                                                │
│ VALIDACIÓN:                                                   │
│ $ printf "00101108097098101114101\n" | ./binary/level2        │
│ Please enter key: Good job.  ✓                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## FLUJO DE TRABAJO RECOMENDADO

```
FASE 1: EXPLORACIÓN (15 minutos)
├─ file binary/levelX          → Tipo de archivo
├─ ./binary/levelX             → Comportamiento
├─ printf "test" | ./binary     → Respuesta
└─ strings binary/levelX        → Búsqueda de pistas

FASE 2: ANÁLISIS (30 minutos)
├─ objdump -d binary/levelX    → Funciones utilizadas
├─ grep funciones importantes  → scanf, strcmp, atoi, etc.
├─ Anotar direcciones de memoria
└─ Entender flujo de ejecución

FASE 3: RECONSTRUCCIÓN (30 minutos)
├─ Recrear el pseudocódigo
├─ Escribir source.c
├─ Validar con pruebas manuales
└─ Compilar y comparar outputs

FASE 4: GENERACIÓN DE PASSWORD (15 minutos)
├─ Encontrar las validaciones
├─ Aplicar inversión del algoritmo (si es encriptado)
├─ Validar con el binario original
└─ Guardar en archivo "password"

TOTAL: ~90 minutos por nivel
```

---

## CHECKLIST DE VALIDACIÓN

### Level 1:
```
✓ Carpeta level1/ existe
✓ level1/password contiene: __stack_check
✓ level1/source.c existe y compila
✓ ./level1_recreado "__stack_check" → "Good job."
✓ ./level1_recreado "prueba" → "Nope."
✓ Outputs son IDÉNTICOS al binario original
```

### Level 2:
```
✓ Carpeta level2/ existe
✓ level2/password contiene: 00101108097098101114101
✓ level2/source.c existe y compila
✓ ./level2_recreado "00101108097098101114101" → "Good job."
✓ ./level2_recreado "prueba" → "Nope."
✓ Validaciones de "00" funcionan
✓ Decodificación numérica correcta
✓ Outputs son IDÉNTICOS al binario original
```

---

## DIAGRAMA: Cómo encontrar la contraseña

### Level 1: Simple
```
binary/level1
    │
    ├─ strings
    │  │
    │  └─ Encuentra: "__stack_check"
    │
    └─ Validar:
       printf "__stack_check" | binary/level1
       → "Good job." ✓
       
PASSWORD ENCONTRADA: __stack_check
```

### Level 2: Complejo
```
binary/level2
    │
    ├─ strings → Encuentra "delabere" (NO es la password)
    │
    ├─ objdump → Encontrar:
    │  • atoi()      → Conversión número
    │  • "00"        → Validación
    │  • strcmp()    → Comparación
    │
    ├─ Entender:
    │  • Input empieza con "00"
    │  • Bloques de 3 dígitos = ASCII codes
    │  • out[0] = 'd' (fijo)
    │  • Resto: decodificar "elabere"
    │
    └─ Invertir algoritmo:
       d = 100 (fijo)
       e = 101  → bloque "101"
       l = 108  → bloque "108"
       a = 097  → bloque "097"
       b = 098  → bloque "098"
       e = 101  → bloque "101"
       r = 114  → bloque "114"
       e = 101  → bloque "101"
       
       PASSWORD = "00" + "101" + "108" + "097" + "098" + "101" + "114" + "101"
       PASSWORD = "00101108097098101114101"
       
       Validar:
       printf "00101108097098101114101" | binary/level2
       → "Good job." ✓
       
PASSWORD ENCONTRADA: 00101108097098101114101
```

---

## HERRAMIENTAS EN ORDEN DE USO

```
1️⃣  file                 → Identificación rápida
2️⃣  ./binary            → Exploración interactiva
3️⃣  strings             → Búsqueda de strings
4️⃣  objdump -d          → Análisis de funciones
5️⃣  gdb (si es necesario) → Debugging detallado
6️⃣  grep                → Búsquedas específicas
7️⃣  gcc                 → Compilar source.c
8️⃣  diff                → Comparar outputs
```

---

## ARQUITECTURA X86 (REFERENCIA)

```
REGISTROS IMPORTANTES (32-bit):
┌─────────────┐
│   EAX       │ Acumulador (resultados, valores de retorno)
│   EBX       │ Base (índices, punteros)
│   ECX       │ Contador (bucles)
│   EDX       │ Datos
│   ESP       │ Puntero de pila (stack pointer)
│   EBP       │ Base de pila (frame pointer)
│   EIP       │ Puntero de instrucción (program counter)
└─────────────┘

INSTRUCCIONES COMUNES:
call XXXX         → Llamar función
ret               → Retorno de función
cmp A, B          → Comparar A con B
je LABEL          → Saltar si igual
jne LABEL         → Saltar si NO igual
mov A, B          → Copiar B en A
push VALUE        → Poner en pila
pop VALUE         → Sacar de pila
```

---

## ENTREGA FINAL REQUERIDA

```
/home/rdel-olm/Desktop/reverse/
│
├── level1/
│   ├── password               ✅ "__stack_check"
│   └── source.c               ✅ (23 líneas)
│
└── level2/
    ├── password               ✅ "00101108097098101114101"
    └── source.c               ✅ (61 líneas)

EXTRAS (documentación):
├── TUTORIAL_LEVEL1.md         📚 (Este archivo)
├── TUTORIAL_LEVEL2.md         📚 (Este archivo)
├── HERRAMIENTAS_REFERENCIA.md 📚 (Comandos)
├── level1_strings.txt         📝
├── level1_disassembly.txt     📝
├── level2_strings.txt         📝
└── level2_disassembly.txt     📝
```

---

## PRÓXIMOS PASOS

### Si necesitas más desafío:
1. Realizar Level3 (aún más complejo que Level2)
2. Modificar binarios y recrearlos
3. Estudiar técnicas de ofuscación de código
4. Aprender sobre protecciones (ASLR, DEP, Stack canaries)

### Si necesitas reforzar conceptos:
1. Leer sobre arquitectura x86 en profundidad
2. Practicar con más binarios
3. Estudiar llamadas al sistema (syscalls)
4. Aprender sobre shellcode

---

## REFERENCIAS ÚTILES

### Documentación online:
- x86 Assembly Reference: https://www.felixcloutier.com/x86/
- GDB Manual: https://sourceware.org/gdb/documentation/
- Capstone Disassembler: http://www.capstone-engine.org/
- PWNTOOLS: https://docs.pwntools.com/

### Libros recomendados:
- "Practical Reverse Engineering" - Bruce Martin
- "The IDA Pro Book" - Chris Eagle
- "Assembly Language for x86 Processors" - Kip Irvine

### Comunidades:
- Crackmes.de
- HackTheBox
- TryHackMe
- OverTheWire

---

**¡Tu proyecto está completo y documentado!** 🎉

**Archivos creados para estudio:**
1. ✅ TUTORIAL_LEVEL1.md - Guía paso a paso del nivel fácil
2. ✅ TUTORIAL_LEVEL2.md - Guía paso a paso del nivel intermedio
3. ✅ HERRAMIENTAS_REFERENCIA.md - Referencia de todas las herramientas
4. ✅ RESUMEN_VISUAL.md - Este documento (visión general del proyecto)
