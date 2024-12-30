
.PHONY: clean
clean:
	rm -rf build
	rm -rf dist	
	rm -rf my_package.egg-info


.PHONY: build 
build:
	python3 setup.py sdist bdist_wheel 

.PHONY: test 
test: 
	echo "do test" 
	pytest 


.PHONY: version 
version: 
	echo "do version" 
	semantic-release version 
	