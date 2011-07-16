
all:

clean:
	rm -rf build/ dist/ factual.egg-info/
	rm -f distribute-*.tar.gz distribute-*.egg
	find . -type f -name *.pyc | xargs rm -f
