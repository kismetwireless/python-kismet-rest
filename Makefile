PYTHON2=python2

all:	
	$(PYTHON2) ./setup.py build
	
install:
	$(PYTHON2) ./setup.py install

clean:
	@-$(PYTHON2) ./setup.py clean

