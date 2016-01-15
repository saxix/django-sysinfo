.PHONY: clean-pyc clean-build docs
DBENGINE?=pg


help:
	@echo "fullclean           remove build artifacts"
	@echo "clean               remove Python file artifacts"
	@echo "qa                  check style with flake8"
	@echo "develop             setup development environment"


.setup-git:
	git config branch.autosetuprebase always
	chmod +x hooks/*
	cd .git/hooks && ln -fs ../../hooks/* .

.init-db:
	@sh -c "if [ '${DBENGINE}' = 'mysql' ]; then mysql -u root -e 'DROP DATABASE IF EXISTS sysinfo;'; fi"
	@sh -c "if [ '${DBENGINE}' = 'mysql' ]; then mysql -u root -e 'CREATE DATABASE IF NOT EXISTS sysinfo;'; fi"

	@sh -c "if [ '${DBENGINE}' = 'pg' ]; then psql -c 'DROP DATABASE IF EXISTS sysinfo;' -U postgres; fi"
	@sh -c "if [ '${DBENGINE}' = 'pg' ]; then psql -c 'CREATE DATABASE sysinfo;' -U postgres; fi"


develop:
	pip install -U pip
	pip install -e .[dev,process]
	$(MAKE) .setup-git


clean:
	rm -fr ./~build dist *.egg-info .coverage pep8.out \
	    coverage.xml flake.out pytest.xml geo.sqlite MANIFEST
	find . -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	find src -name django.mo | xargs rm -f


fullclean:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -fr .tox
	find . -name *.sqlite -prune | xargs rm -rf
	$(MAKE) clean

qa:
	flake8 src/django_sysinfo tests
	isort -rc src/django_sysinfo tests/ --check-only
	check-manifest

docs:
	#rm -f docs/django-sysinfo.rst
	#rm -f docs/modules.rst
	#sphinx-apidoc -o docs/ django_sysinfo
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open ./~build/docs/html/index.html
