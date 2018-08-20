python setup.py sdist bdist_wheel --universal
twine upload dist/*
rm -Rf dist build Fancy_progressbar.egg-info