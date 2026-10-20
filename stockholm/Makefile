NAME = stockholm
SCRIPT = stockholm.py

all: install

install:
	@echo "Instalando dependencias necesarias..."
	pip3 install cryptography

clean:
	@echo "Limpiando archivos temporales..."
	rm -rf __pycache__
	rm -rf *.pyc

fclean: clean
	@echo "Limpiando claves generadas..."
	rm -f clave.key

re: fclean all

.PHONY: all install clean fclean re