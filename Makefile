maint:
	pre-commit autoupdate
	pip-compile -U requirements/ci.in
	pip-compile -U requirements/dev.in

upload:
	make clean
	python setup.py sdist bdist_wheel && twine upload -s dist/*

clean:
	python setup.py clean --all
	pyclean .
	rm -rf tests/__pycache__ idnow_responses/__pycache__ Image9.png htmlcov docs/_build dist dont_commit_merged.pdf dont_commit_writer.pdf idnow_responses.egg-info idnow_responses_pdfLocation.txt .pytest_cache .mypy_cache .benchmarks

test:
	pytest tests --cov --cov-report term-missing -vv --cov-report html --durations=3 --timeout=60 idnow_responses
