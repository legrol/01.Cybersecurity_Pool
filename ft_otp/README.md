# ft_otp

Implementacion de generacion de contrasenas temporales de 6 digitos a partir de una clave hexadecimal.

El proyecto sigue el flujo del subject:
- `-g`: guarda una clave hexadecimal (minimo 64 caracteres) en `ft_otp.key` cifrado.
- `-k`: genera una OTP temporal usando la clave cifrada.

La OTP se calcula usando HOTP (RFC 4226) como componente fundamental.
Para modo temporal (TOTP), el contador HOTP se obtiene de la ventana de tiempo de 30 segundos.

## Algoritmo

- **HOTP (RFC 4226)**: El nucleo criptografico que genera 6 digitos con HMAC-SHA1 y truncamiento dinamico.
- **TOTP (RFC 6238)**: Aplica HOTP con contador temporal (ventana de 30 segundos = 30-second window).
- **Claves aleatorias**: Salt y nonce aleatoria para cada cifrado garantiza entropia.
- **Truncamiento dinamico**: Extrae 4 bytes del hash HMAC de forma segura (RFC 4226 §5.3).

## Gestion de excepciones

El programa valida:
- Existencia y legibilidad de archivos → termina con `ft_otp: error: ...` si falla.
- Formato hexadecimal (64+ caracteres) → valida antes de guardar y tras descifrar.
- Integridad de datos: Si falla descifrado o autenticacion, muestra `Incorrect password.` y exit(1).

Todas las excepciones se manejan con `try/except`, terminando el programa con exit(1).

## Requisitos

- Python 3 (sin instalar paquetes extra)

No necesita `pip install` para funcionar con `-g` y `-k`.

```bash
python3 ft_otp.py -h
```

## Uso

Nota: las banderas `-g`, `-k` y `-qr` son excluyentes (se usa una por ejecucion).

Mostrar ayuda:

```bash
python3 ft_otp.py -h
```

Generar fichero cifrado con la clave:

```bash
python3 ft_otp.py -g key.hex
```

Generar OTP desde fichero cifrado:

```bash
python3 ft_otp.py -k ft_otp.key
```

Mostrar QR de la clave secreta:

```bash
python3 ft_otp.py -qr ft_otp.key
```

Si `qrcode-terminal` no esta disponible, el programa muestra la clave en texto como alternativa.

Internamente, el modulo de QR se carga con import dinamico. Asi, el programa no falla al arrancar en maquinas donde esa libreria no esta instalada.

## Formato de la clave

La clave de entrada debe cumplir:
- Solo caracteres hexadecimales: `[0-9a-fA-F]`
- Longitud minima: 64 caracteres

Ejemplo para generar una clave valida de 64 caracteres:

```bash
python3 -c "print('0123456789abcdef' * 4)" > key.hex
```

## Verificacion con oathtool

Si tienes `oathtool`, puedes comparar el resultado:

```bash
oathtool --totp "$(cat key.hex)"
```

Nota: el codigo puede cambiar cada 30 segundos, por lo que la comparacion debe hacerse en la misma ventana temporal.
