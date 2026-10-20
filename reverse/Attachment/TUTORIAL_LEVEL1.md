# TUTORIAL COMPLETO: Reverse Engineering Level1

## ¿QUÉ ES REVERSE ENGINEERING?

Reverse Engineering es el proceso de **analizar** un programa compilado (binario) **sin tener el código fuente** para:
1. Entender qué hace
2. Encontrar contraseñas o secretos
3. Recrear el código original en C

---

## EL PUNTO DE PARTIDA: Un binario desconocido

**Tenemos:** `binary/level1` (ejecutable compilado)
**No tenemos:** El código fuente (`.c`)
**Objetivo:** 
- Encontrar la contraseña
- Recrear `source.c`

---

## PASO 1: IDENTIFICAR EL TIPO DE ARCHIVO

### Comando:
```bash
file binary/level1
```

### Resultado:
```
binary/level1: ELF 32-bit LSB pie executable, Intel 80386, version 1 (SYSV), 
dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=..., 
for GNU/Linux 3.2.0, not stripped
```

### Qué significa:
- **ELF** = Formato de ejecutable Linux
- **32-bit** = Arquitectura x86 (procesador 32 bits)
- **executable** = Es un programa que puedo ejecutar
- **not stripped** = Contiene símbolos de debugging (ayuda en reverse engineering)

---

## PASO 2: EJECUTAR EL BINARIO (prueba inicial)

### Comando:
```bash
./binary/level1
```

### Lo que sucede:
```
Please enter key: █
```

**Conclusión:** El programa pide una entrada del usuario llamada "key"

---

## PASO 3: PROBAR CON UNA CONTRASEÑA INCORRECTA

### Comando:
```bash
printf "prueba\n" | ./binary/level1
```

### Resultado:
```
Please enter key: Nope.
```

**Conclusión:** Si la contraseña es incorrecta, imprime "Nope."

---

## PASO 4: BUSCAR STRINGS (¡Herramienta CLAVE!)

### ¿Qué es `strings`?
- Extrae todos los **textos legibles** almacenados en el binario
- Es muy útil porque muchas contraseñas/mensajes no están encriptados

### Comando:
```bash
strings binary/level1
```

### Output completo (87 líneas):
```
/lib/ld-linux.so.2
_IO_stdin_used
__isoc99_scanf
__cxa_finalize
__libc_start_main
printf
strcmp
libc.so.6
GLIBC_2.7
GLIBC_2.1.3
GLIBC_2.34
GLIBC_2.0
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
__stack_check              👈 ¡¡¡CONTRASEÑA!!!
Please enter key: 
Good job.
Nope.
...
```

### Análisis de strings útiles:
```
__stack_check      ← Probablemente la contraseña
Please enter key:  ← Mensaje inicial
Good job.          ← Éxito
Nope.              ← Fracaso
strcmp             ← Función que compara strings
printf             ← Función que imprime
scanf              ← Función que lee entrada
```

**Hipótesis:** El programa compara lo que escribes con `__stack_check` (strcmp)

---

## PASO 5: VALIDAR LA CONTRASEÑA

### Comando:
```bash
printf "__stack_check\n" | ./binary/level1
```

### Resultado:
```
Please enter key: Good job.
```

✅ **¡CONTRASEÑA ENCONTRADA: `__stack_check`**

---

## PASO 6: ANALIZAR CON OBJDUMP (Código máquina → Assembly)

### ¿Qué es objdump?
- Muestra el **código máquina desensambblado** (assembly)
- Permite ver exactamente qué hace el programa a nivel CPU

### Comando:
```bash
objdump -d binary/level1 | grep -A 50 "<main>:"
```

### Output (las líneas importantes):
```assembly
000011c0 <main>:
    11c0:       55                      push   %ebp
    11c1:       89 e5                   mov    %esp,%ebp
    11c3:       53                      push   %ebx
    11c4:       81 ec 84 00 00 00       sub    $0x84,%esp
    ... (inicialización)
    
    1227:       e8 44 fe ff ff          call   1070 <__isoc99_scanf@plt>
                                        👆 Lee entrada (scanf)
    
    123c:       e8 ff fd ff ff          call   1040 <strcmp@plt>
                                        👆 Compara strings (strcmp)
    
    1241:       83 f8 00                cmp    $0x0,%eax
                                        👆 ¿Son iguales? (cmp result, 0)
    
    1244:       0f 85 16 00 00 00       jne    1260 <main+0xa0>
                                        👆 Si NO son iguales, salta a error
    
    1256:       e8 05 fe ff ff          call   1060 <printf@plt>
                                        👆 Imprime "Good job."
    
    126c:       e8 ef fd ff ff          call   1060 <printf@plt>
                                        👆 Imprime "Nope."
    
    1271:       31 c0                   xor    %eax,%eax
    1273:       81 c4 84 00 00 00       add    $0x84,%esp
    1279:       5b                      pop    %ebx
    127a:       5d                      pop    %ebp
    127b:       c3                      ret
```

### Lectura del código:
1. **Inicialización** → Reserva espacio en stack (84 bytes = buffer de 108 caracteres?)
2. **scanf** → Lee lo que escribes
3. **strcmp** → Compara dos strings
4. **cmp result, 0** → ¿El resultado fue 0? (0 = strings iguales)
5. **jne** → Si no es igual (jne = Jump if Not Equal), vamos a mostrar "Nope."
6. **printf** → Imprime "Good job." o "Nope."

---

## PASO 7: GDB (DEBUGGER) - Ejecución paso a paso

### ¿Qué es gdb?
- **Debugger interactivo** que permite:
  - Ejecutar línea por línea
  - Ver variables
  - Inspeccionar memoria
  - Ver registros CPU

### Comandos básicos de gdb:
```bash
gdb ./binary/level1

(gdb) break main              # Parar en función main
(gdb) run                      # Ejecutar
(gdb) next                     # Siguiente línea
(gdb) step                     # Entrar en función
(gdb) print $eax               # Ver contenido de registro
(gdb) x/s $esp                 # Ver memoria como string
(gdb) continue                 # Continuar ejecución
(gdb) quit                     # Salir
```

---

## PASO 8: RECREAR EL SOURCE.C

Basándonos en lo que aprendimos:

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    // Buffer para almacenar lo que escribe el usuario
    char input[108];
    
    // La contraseña correcta (encontrada con strings)
    const char expected[] = "__stack_check";

    // Mostrar el mensaje inicial
    printf("Please enter key: ");
    
    // Leer lo que escribe el usuario (acotado)
    if (scanf("%107s", input) != 1)
    {
        printf("Nope.\n");
        return 0;
    }

    // Comparar: si input == "__stack_check"
    if (strcmp(input, expected) == 0)
    {
        printf("Good job.\n");
    }
    else
    {
        printf("Nope.\n");
    }

    return 0;
}
```

### Explicación línea por línea:

| Línea | ¿De dónde viene? | Explicación |
|-------|-----------------|------------|
| `char input[108];` | objdump: stack reserve 0x84 (132 bytes) → 108 caracteres | Buffer para la entrada |
| `__stack_check` | strings: encontramos este string | La contraseña |
| `printf("Please enter key: ");` | strings: encontramos este texto | Mensaje inicial |
| `scanf("%107s", input)` | Lectura segura en la recreación | Lee del usuario sin overflow |
| `strcmp(input, expected)` | objdump: call 1040 <strcmp> | Compara strings |
| `== 0` | objdump: cmp $0x0,%eax | 0 = strings iguales |
| `printf("Good job.\n");` | strings: encontramos "Good job." | Éxito |
| `printf("Nope.\n");` | strings: encontramos "Nope." | Fallo |

---

## PASO 9: VERIFICACIÓN - Compilar y probar

### Compilar nuestro código recreado:
```bash
gcc -o level1_recreado level1/source.c
```

### Prueba 1: Contraseña correcta
```bash
printf "__stack_check\n" | ./level1_recreado
```
**Output:**
```
Please enter key: Good job.
```

### Prueba 2: Contraseña incorrecta
```bash
printf "prueba\n" | ./level1_recreado
```
**Output:**
```
Please enter key: Nope.
```

### Prueba 3: Comparar con original
```bash
printf "__stack_check\n" | ./binary/level1
printf "__stack_check\n" | ./level1_recreado
```

✅ **¡AMBOS PRODUCEN EL MISMO OUTPUT!**

---

## RESUMEN: HERRAMIENTAS USADAS

| Herramienta | Propósito | Comando |
|------------|----------|---------|
| `file` | Identificar tipo | `file binary/level1` |
| `./binary` | Ejecutar | `./binary/level1` |
| `strings` | Buscar textos | `strings binary/level1` |
| `objdump` | Desensamblar | `objdump -d binary/level1` |
| `gdb` | Debugger | `gdb binary/level1` |
| `printf \| ./binary` | Automatizar entrada | `printf "test\n" \| ./binary/level1` |

---

## DIAGRAMA DEL FLUJO DE REVERSE ENGINEERING

```
┌─────────────────────────────────────────────────────┐
│     BINARIO DESCONOCIDO: binary/level1              │
│     (Sin código fuente, compilado, ejecutable)      │
└────────────────┬────────────────────────────────────┘
                 │
                 ├──→ file               (¿Qué es?)
                 │    Resultado: ELF 32-bit executable
                 │
                 ├──→ ./binary/level1    (¿Qué hace?)
                 │    Resultado: Pide "Please enter key: "
                 │
                 ├──→ strings            (¿Qué strings tiene?)
                 │    ✓ Resultado: "__stack_check", "Good job.", "Nope."
                 │    → ENCONTRAMOS LA CONTRASEÑA
                 │
                 ├──→ printf ... | ./binary (¿Funciona?)
                 │    ✓ Resultado: "Good job." con "__stack_check"
                 │    → CONTRASEÑA VALIDADA
                 │
                 ├──→ objdump -d         (¿Cómo funciona?)
                 │    ✓ Resultado: scanf, strcmp, printf
                 │    → LÓGICA COMPRENDIDA
                 │
                 └──→ Crear source.c
                      ✓ Replica exactamente la funcionalidad
```

---

## LECCIONES CLAVE

### 1. **La mayoría de contraseñas están en STRINGS**
```
NO está encriptada → strings las encuentra fácilmente
```

### 2. **OBJDUMP muestra qué funciones se usan**
```
scanf     → Lee entrada
strcmp    → Compara strings
printf    → Imprime
```

### 3. **La comparación en assembly es crucial**
```
cmp $0x0,%eax    → "¿Es el resultado igual a 0?"
jne              → "Si NO es igual, salta"
```

### 4. **Siempre validar tu hipótesis**
```
Encontré "__stack_check" → La probé → Funcionó
```

### 5. **El buffer size importa**
```
Stack reserve = 0x84 (132 bytes) → char input[108]
```

---

## SIGUIENTE NIVEL: Level2 (MÁS COMPLICADO)

Level2 no es tan simple. La contraseña:
- Debe empezar con `00`
- Se lee en bloques de 3 dígitos
- Cada bloque se convierte a ASCII
- Se construye una cadena
- Se compara con `delabere`

**Password:** `00101108097098101114101`

Decodificación:
```
00  101  108 097 098 101 114 101
    e    l   a   b   e   r   e
    
Resultado: "delabere"
```

---

## RESUMEN FINAL

**¿Cómo sacamos la contraseña sin código fuente?**

1. ✅ Ejecutamos el binario → Vemos que pide entrada
2. ✅ Usamos `strings` → Encontramos "__stack_check"
3. ✅ Probamos la contraseña → Validamos que funciona
4. ✅ Analizamos con `objdump` → Vemos strcmp, scanf, printf
5. ✅ Recreamos en C → Código idéntico al original

**¡Eso es Reverse Engineering!**
