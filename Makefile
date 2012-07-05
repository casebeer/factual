
# Makefile just for cleanup tasks

all:

clean:
	rm -rf build/ dist/ factual.egg-info/
	rm -rf *.egg
	rm -f distribute-*.tar.gz distribute-*.egg
	find . -type f -name *.pyc | xargs rm -f

