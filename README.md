# Cybersecurity Pool

![Cybersecurity Pool illustration](zz_Others/cybersecurity-pool.svg)

A collection of hands-on cybersecurity projects developed during the 42 bootcamp. The pool covers analysis, cryptography, networking, and web security, with documentation and evaluation material for each module.

> **Responsible use:** These projects are for educational purposes. Run tests only on systems you own, local labs, or environments where you have explicit authorization. In particular, `inquisitor` and `vaccine` can generate test traffic, and `stockholm` encrypts files.

## Projects

| Project | Area | Overview |
| --- | --- | --- |
| [Arachnida](Arachnida/README.md) | Web analysis and metadata | `spider.py` downloads images from web pages; `scorpion.py` inspects image metadata. |
| [ft_otp](ft_otp/README.md) | Cryptography and authentication | Generates time-based one-time passwords from a hexadecimal key. |
| [ft_onion](ft_onion/README.md) | Networking and privacy | Hosts a Tor hidden service with Nginx and SSH in a configurable environment. |
| [Inquisitor](inquisitor/README.md) | Networking and traffic analysis | A lab tool for ARP poisoning and observing filenames in FTP traffic. |
| [Reverse](reverse/README.md) | Reverse engineering | Analyzes binaries and reconstructs the logic behind multiple levels. |
| [Stockholm](stockholm/README.md) | Cryptography and malware | An educational file-encryption and recovery simulation scoped to a test folder. |
| [Vaccine](vaccine/README.md) | Web security | Tests for SQL injection vulnerabilities and includes a local demo server. |

## Getting started

Each project has its own requirements and setup instructions. Open the project directory and follow its README; there is no single installation process for the entire pool.

```bash
cd Arachnida
```

Some projects include additional guides, evaluation commands, or Docker labs. Read the project documentation before running tools or setting up an environment.

## Repository structure

```text
.
├── Arachnida/
├── ft_otp/
├── ft_onion/
├── inquisitor/
├── reverse/
├── stockholm/
├── vaccine/
├── zz_Others/
├── zz_Subjects _Cyber/
└── zz_Subject_Corrections/
```

The `zz_Subjects _Cyber` and `zz_Subject_Corrections` directories contain project subjects and reference corrections.

## Technologies and concepts

Python · C · Linux · Docker · Tor · Nginx · SSH · OTP · traffic analysis · reverse engineering · web security.

---

Personal learning projects completed as part of the 42 Cybersecurity Pool.