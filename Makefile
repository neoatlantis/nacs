all: nacs_start.py
	python3.6 -m transcrypt -n nacs_start.py

test:
	python -m SimpleHTTPServer 8888
