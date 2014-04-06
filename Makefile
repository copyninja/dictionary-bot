travis:
	nosetests -s --with-coverage --cover-package=dictbot
	flake8 dictbot

clean:
	find . -name "*.pyc" -exec rm {} \;
	find -name __pycache__ -delete
tox:
	tox

flake:
	flake8 dictbot
