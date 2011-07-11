
all:

clean:
	rm -rf build/ dist/ factual.egg-info/
	find . -type f -name *.pyc | xargs rm -f
