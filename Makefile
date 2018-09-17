.PHONY: install shell run 

run:
	source env/bin/activate; \
	python3.6 src/main.py;

shell:
	source env/bin/activate; \
	bpython;


install:
	python3 -m venv --prompt "env" --system-site-packages env
	source env/bin/activate; \
	pip3 install -r Requirements.txt;


