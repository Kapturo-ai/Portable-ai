.PHONY: inspect validate test build

inspect:
	python3 scripts/sticker-card.py inspect .

validate:
	python3 scripts/sticker-card.py validate .

test:
	python3 -m unittest discover -s tests -p 'test_*.py'

build:
	python3 scripts/sticker-card.py build . --out ./dist
