all:
	python3.6 -m transcrypt -n nacs_start.py

test:
	python -m SimpleHTTPServer 8888

build:
	python3.6 -m transcrypt nacs_start.py
