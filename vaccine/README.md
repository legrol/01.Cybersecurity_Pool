![ [python_version](https://img.shields.io/badge/python-3.9%20%7C%203.10-blue) ](https://img.shields.io/badge/python-3.9%20%7C%203.10-blue)
    # vaccine

_____________________________________
 Bootcamp Cybersecurity | 42 Málaga
 
     v   a   c   c   i   n   e
_____________________________________

## What this script does?
This script is a battery of tests to run against a given `URL` to be able to detect [SQL injection](https://en.wikipedia.org/wiki/SQL_injection) vulnerabilities. It detect type of database engine. The tests can be based on several types: union, error, boolean, time and even blind.

In case a website is confirmed to be vulnerable, the following can be obtained:
- The vulnerable parameters.
- The payload used.
- Database names.
- Table names.
- Column names.
- Complete database dump.

The data will be stored in a file.

It is also possible to perform a `SQL injection` by providing a `URL` as a parameter.

## What is SQL injection?
SQL Injection is the injection of SQL commands to alter the behaviour of a program and execute commands on the database. The impact SQL injection can have on a business is far reaching. A successful attack may result in the unauthorized viewing of user lists, the deletion of entire tables and, in certain cases, the attacker gaining administrative rights to a database, all of which are highly detrimental to a business.

## Arguments:
- Option -o : Archive file, if not specified it will be stored in a default one.
- Option -X : Type of request, if not specified GET will be used.
- Option -c : Login cookie if needed.
- Option -u : User-Agent, if not specified it will be a default one.
```bash
python3 vaccine.py [-oXcu] URL
```

## Bonus part:
- Wider range of database engines.
- Wider range of SQL injection methods.
- The tool allows you to edit various parameters of the request, e.g. the User-Agent and Setup custom cookies.

## How to test it? (Natively without Docker)
To test our script natively without needing Docker or external vulnerable machines, we have included a local dummy server (`dummy_server.py`) that simulates a vulnerable page in Python. This is intended to facilitate the project's presencial evaluation at 42 campuses.

**1. Start the vulnerable test mock-server:**
Open a terminal and run the test server:
```bash
```bash
python3 dummy_server.py
```
*(This will try `http://127.0.0.1:8080/` first and fall back to `http://127.0.0.1:8081/` if needed.)*

**2. Attack the fake dummy server using Vaccine:**
In a separate terminal tab, you can execute the different evaluation scenarios:

Test standard SQL injection:
```bash
python3 vaccine.py http://127.0.0.1:8080/
python3 vaccine.py http://127.0.0.1:8081/
```

Test passing output towards a specific file:
```bash
python3 vaccine.py -o sql_results.log http://127.0.0.1:8080/
python3 vaccine.py -o sql_results.log http://127.0.0.1:8081/
```

Test forcing a POST method:
```bash
python3 vaccine.py -X POST http://127.0.0.1:8080/
python3 vaccine.py -X POST http://127.0.0.1:8081/
```

Test inserting an arbitrary User-Agent and custom cookie (Bonus):
```bash
python3 vaccine.py -u "AgentPiscine42" -c "session=admin_123" http://127.0.0.1:8080/
python3 vaccine.py -u "AgentPiscine42" -c "session=admin_123" http://127.0.0.1:8081/
```

May 2023

<p align="center"> <img src="./vaccine.jpeg" alt="image" width="456" /> </p>
