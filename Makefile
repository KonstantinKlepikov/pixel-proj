test:
	python -m pytest tests -x -s -v

run:
	python src/main.py

serve:
	sh watch.sh
