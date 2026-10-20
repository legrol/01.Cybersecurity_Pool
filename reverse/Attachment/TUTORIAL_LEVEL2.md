# TUTORIAL COMPLETO: Reverse Engineering Level2

## INTRODUCCIÓN: ¿Por qué es más difícil que Level1?

**Level1:** Comparación simple
```
Input → strcmp("input", "__stack_check") → Good/Nope
```

**Level2:** Un algoritmo más complejo
```
Input → Validar formato → Decodificar bloques → Construir cadena → strcmp → Good/Nope
```

---

## PASO 1: EJECUTAR EL BINARIO (Prueba inicial)

### Comando:
```bash
./binary/level2
```

### Resultado:
```
Please enter key: █
```

**Igual que Level1:** Pide una "key"

---

## PASO 2: BUSCAR STRINGS

### Comando:
```bash
strings binary/level2 | grep -E "(Please|Good|Nope|delabere)"
```

### Output:
```
Nope.
Good job.
Please enter key: 
delabere     👈 ¡¡¡STRING IMPORTANTE!!!
```

### Análisis:
- `delabere` aparece en el código → Probablemente la cadena a comparar
- Pero esta vez **NO es la contraseña directa**
- Level2 es más sofisticado

---

## PASO 3: PRUEBA DIRECTA (no funciona)

### Intento 1: Usar "delabere" directamente
```bash
printf "delabere\n" | ./binary/level2
```

**Resultado:**
```
Please enter key: Nope.
```

❌ No funciona. La contraseña no es simplemente "delabere"

---

## PASO 4: ANALIZAR CON OBJDUMP (El algoritmo)

### Comando:
```bash
objdump -d binary/level2 | grep -A 100 "<main>:"
```

### LÍNEAS RELEVANTES (solo lo importante):
```assembly
000012d0 <main>:
    # ====== PRINTF Y SCANF ======
    12f6:       call   1060 <printf@plt>            # Print "Please enter key: "
    130e:       call   10c0 <__isoc99_scanf@plt>    # scanf("%23s", input)

    # ====== VALIDACIÓN: input[0] == '0' ======
    132c:       movsbl -0x34(%ebp),%ecx            # carga input[0]
    1330:       mov    $0x30,%eax                  # '0' = 0x30
    1335:       cmp    %ecx,%eax
    1337:       je     1345                        # continuar si OK
    1340:       call   1220 <no>                   # error si NO

    # ====== VALIDACIÓN: input[1] == '0' ======
    1345:       movsbl -0x35(%ebp),%ecx            # carga input[1]
    1349:       mov    $0x30,%eax
    134e:       cmp    %ecx,%eax
    1350:       je     135e                        # continuar si OK
    1359:       call   1220 <no>                   # error si NO

    # ====== INICIALIZACIÓN ======
    1392:       call   10b0 <memset@plt>           # memset(out, 0, 9)
    1397:       movb   $0x64,-0x1d(%ebp)           # out[0] = 'd' (0x64)
    139f:       movl   $0x2,-0x14(%ebp)            # i = 2
    13a6:       movl   $0x1,-0x10(%ebp)            # j = 1

    # ====== BUCLE: strlen(out) < 8 Y i < strlen(input) ======
    13b7:       call   10a0 <strlen@plt>           # strlen(out)
    13c0:       cmp    $0x8,%ecx                   # ¿strlen(out) >= 8?
    13dc:       call   10a0 <strlen@plt>           # strlen(input)
    13e6:       cmp    %ecx,%eax                   # ¿i >= strlen(input)?
    13f3:       jne    13fe                        # entrar en bucle si OK
    13f9:       jmp    144a                        # salir si ambas NO cumplen

    # ====== PROCESAR BLOQUE: block[0-2] = input[i:i+3] ======
    1404:       mov    -0x35(%ebp,%eax,1),%al      # input[i]
    1408:       mov    %al,-0x39(%ebp)             # block[0]
    140e:       mov    -0x34(%ebp,%eax,1),%al      # input[i+1]
    1412:       mov    %al,-0x38(%ebp)             # block[1]
    1418:       mov    -0x33(%ebp,%eax,1),%al      # input[i+2]
    141c:       mov    %al,-0x37(%ebp)             # block[2]

    # ====== CONVERTIR: atoi(block) -> out[j] ======
    1422:       mov    %eax,(%esp)                 # parámetro: &block
    1425:       call   10d0 <atoi@plt>             # atoi(block) → eax
    142a:       mov    %al,%cl                     # cl = char(atoi)
    142f:       mov    %cl,-0x1d(%ebp,%eax,1)      # out[j] = cl

    # ====== INCREMENTOS: i += 3, j += 1 ======
    1436:       add    $0x3,%eax                   # i += 3
    1439:       mov    %eax,-0x14(%ebp)
    143f:       add    $0x1,%eax                   # j += 1
    1442:       mov    %eax,-0x10(%ebp)
    1445:       jmp    13ad                        # volver al bucle

    # ====== CIERRE Y STRCMP ======
    1450:       movb   $0x0,-0x1d(%ebp,%eax,1)     # out[j] = '\0'
    1465:       call   1040 <strcmp@plt>           # strcmp(out, "delabere")
    146a:       cmp    $0x0,%eax
    146d:       jne    1480                        # si NO iguales → no()

    # ====== RESULTADO ======
    1476:       call   12a0 <ok>                   # "Good job."
    1483:       call   1220 <no>                   # "Nope."
```

### Tabla de funciones en Level2:
| Función | Propósito |
|---------|-----------|
| `printf()` | Imprime "Please enter key: " |
| `scanf("%23s")` | Lee máximo 23 caracteres |
| `atoi()` | Convierte string a número (ej: "101" → 101) |
| `strlen()` | Obtiene longitud de string |
| `strcmp()` | Compara strings |

---

## PASO 5: RECONSTRUIR LA LÓGICA

### El algoritmo en pseudocódigo:

```
1. Leer input (máximo 23 caracteres)

2. VALIDACIÓN:
   - ¿input[0] == '0'?
   - ¿input[1] == '0'?
   - Si NO → "Nope."

3. PROCESAMIENTO:
   out[0] = 'd'  (primer carácter fijo)
   i = 2         (empezar a leer desde posición 2 del input)
   j = 1         (índice donde escribir en output)
   
   MIENTRAS strlen(out) < 8 Y i < strlen(input):
       bloque = input[i:i+3]      (coger 3 caracteres)
       numero = atoi(bloque)       (convertir "101" a 101)
       out[j] = chr(numero)        (convertir número a carácter ASCII)
       i += 3
       j += 1

4. COMPARACIÓN:
   ¿out == "delabere"?
   - SÍ  → "Good job."
   - NO  → "Nope."
```

---

## PASO 6: OBTENER LA CONTRASEÑA (INGENIERÍA INVERSA)

Sabemos que:
- out[0] = 'd' (fijo)
- out debe ser = "delabere" (8 caracteres)
- out[1-7] = "elabere"

### Conversión ASCII → Números:

```
d = 100  (no llega del input, es fijo)
e = 101
l = 108
a = 097
b = 098
e = 101
r = 114
e = 101
```

### Construcción de la contraseña:

```
Inicio: "00" (obligatorio)
+ "101" (e)
+ "108" (l)
+ "097" (a)
+ "098" (b)
+ "101" (e)
+ "114" (r)
+ "101" (e)

═══════════════════════════════════
CONTRASEÑA: 00101108097098101114101
═══════════════════════════════════
```

---

## PASO 7: VALIDAR LA CONTRASEÑA

### Prueba:
```bash
printf "00101108097098101114101\n" | ./binary/level2
```

### Resultado:
```
Please enter key: Good job.
```

✅ **¡CONTRASEÑA ENCONTRADA Y VALIDADA!**

---

## PASO 8: RECREAR EL SOURCE.C

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

static void no(void)
{
    puts("Nope.");
    exit(1);
}

static void ok(void)
{
    puts("Good job.");
}

int main(void)
{
    char input[24];        // Máximo 23 caracteres + null terminator
    char out[9];           // "delabere" = 8 caracteres + null
    char block[4];         // Buffer para 3 dígitos + null
    int i;
    int j;

    printf("Please enter key: ");
    
    // Leer máximo 23 caracteres del usuario
    if (scanf("%23s", input) != 1)
        no();

    // VALIDACIÓN: ¿Empieza con "00"?
    if (input[0] != '0')
        no();
    if (input[1] != '0')
        no();

    fflush(stdin);

    // INICIALIZACIÓN
    memset(out, 0, 9);      // Limpiar buffer
    out[0] = 'd';           // Primer carácter fijo
    i = 2;                  // Empezar a leer desde posición 2
    j = 1;                  // Empezar a escribir en posición 1

    // BUCLE: Procesar bloques de 3 dígitos
    while (strlen(out) < 8 && i + 2 < (int)strlen(input))
    {
        // Extraer 3 dígitos consecutivos
        block[0] = input[i];
        block[1] = input[i + 1];
        block[2] = input[i + 2];
        block[3] = '\0';

        // Convertir a número, luego a carácter ASCII
        out[j] = (char)atoi(block);
        
        i += 3;  // Siguiente bloque
        j += 1;  // Siguiente posición en output
    }

    out[j] = '\0';  // Null terminator

    // COMPARACIÓN
    if (strcmp(out, "delabere") == 0)
        ok();
    else
        no();

    return 0;
}
```

### Explicación línea por línea:

| Sección | Explicación |
|---------|------------|
| `scanf("%23s")` | Lee máximo 23 caracteres (de objdump) |
| `input[0] != '0'` | Validar que empiece con '0' |
| `input[1] != '0'` | Validar que el segundo sea '0' |
| `out[0] = 'd'` | El primer carácter SIEMPRE es 'd' |
| `i = 2` | Empezamos a procesar desde la posición 2 |
| `block[0-2]` | Coger 3 caracteres consecutivos |
| `atoi(block)` | Convertir "101" → 101 |
| `(char)atoi()` | Convertir número ASCII a carácter |
| `strcmp(out, "delabere")` | Comparar el resultado |

---

## PASO 9: VERIFICACIÓN

### Compilar:
```bash
gcc -o level2_recreado level2/source.c
```

### Prueba 1: Contraseña correcta
```bash
printf "00101108097098101114101\n" | ./level2_recreado
```
**Output:**
```
Please enter key: Good job.
```

### Prueba 2: Contraseña incorrecta
```bash
printf "00\n" | ./level2_recreado
```
**Output:**
```
Please enter key: Nope.
```

### Prueba 3: Sin empezar en "00"
```bash
printf "99101108097098101114101\n" | ./level2_recreado
```
**Output:**
```
Please enter key: Nope.
```

✅ **¡TODOS LOS TESTS PASAN!**

---

## DIAGRAMA: Decodificación de la contraseña

```
CONTRASEÑA ENCRIPTADA: 00101108097098101114101
                       │││││││││││││││││││││││││
                       ││││└─────┘└─────┘└─────┘ Bloques de 3 dígitos
                       │││└─ "00" (validación obligatoria)
                       
PROCESAMIENTO:
                       
Input[0] = '0' (validar)
Input[1] = '0' (validar)

Input[2:5]   = "101" → atoi("101") = 101   → chr(101) = 'e'
Input[5:8]   = "108" → atoi("108") = 108   → chr(108) = 'l'
Input[8:11]  = "097" → atoi("097") = 97    → chr(97)  = 'a'
Input[11:14] = "098" → atoi("098") = 98    → chr(98)  = 'b'
Input[14:17] = "101" → atoi("101") = 101   → chr(101) = 'e'
Input[17:20] = "114" → atoi("114") = 114   → chr(114) = 'r'
Input[20:23] = "101" → atoi("101") = 101   → chr(101) = 'e'

OUTPUT CONSTRUIDO:
out[0] = 'd' (fijo)
out[1-7] = "elabere"
═════════════════════════════════════════════════
RESULTADO FINAL: "delabere" ✓
```

---

## COMPARACIÓN: Level1 vs Level2

| Aspecto | Level1 | Level2 |
|---------|--------|--------|
| **Tipo** | Comparación simple | Algoritmo de decodificación |
| **Contraseña evidente** | SÍ (strings) | NO (encriptada en hex) |
| **Funciones** | printf, scanf, strcmp | printf, scanf, atoi, strcmp, strlen, memset |
| **Validación** | Ninguna | Debe empezar con "00" |
| **Complejidad** | ⭐ Baja | ⭐⭐⭐ Alta |
| **Dificultad RE** | Principiante | Intermedio |

---

## LECCIONES CLAVE DE LEVEL2

### 1. **La contraseña NO siempre está visible en strings**
```
strings muestra "delabere" pero NO la contraseña numérica
```

### 2. **Necesitas RECONSTRUIR la lógica**
```
Lógica: Decodificar bloques de 3 dígitos
Inversa: Codificar caracteres como bloques de 3 dígitos
```

### 3. **Validaciones especiales**
```
Debe empezar con "00"
Bloques de 3 dígitos
Máximo 23 caracteres
```

### 4. **ASCII es fundamental**
```
Tabla ASCII:
a=97, b=98, d=100, e=101, l=108, r=114
```

### 5. **El algoritmo se descubre en objdump**
```
atoi      → Conversión número
strlen    → Longitud
memset    → Inicializar buffer
```

---

## RESUMEN FINAL

**Proceso de Reverse Engineering Level2:**

1. ✅ Ejecutar binario → Ver que pide entrada
2. ✅ Buscar strings → Encontrar "delabere"
3. ✅ Probar directamente → No funciona (no es la contraseña)
4. ✅ Analizar objdump → Encontrar atoi(), validación "00"
5. ✅ Reconstruit lógica → Algoritmo de decodificación
6. ✅ Invertir algoritmo → Codificar "delabere" a números
7. ✅ Crear contraseña → "00101108097098101114101"
8. ✅ Validar → Funciona correctamente
9. ✅ Recrear source.c → Código idéntico al original

---

## HERRAMIENTAS UTILIZADAS

| Herramienta | Propósito |
|------------|-----------|
| `strings` | Encontrar textos clave |
| `objdump` | Ver funciones y flujo |
| `gdb` | Debugging paso a paso |
| `printf \| ./binary` | Automatizar entrada |
| `gcc -o` | Compilar source.c |
| `printf \| ./compiled` | Verificar |

---
