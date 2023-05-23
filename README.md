Theresa (Machine Learning Webservice) <sup>![Python Version Badge][Python Version Badge]</sup>
==============================================================================================

A fast [prototyping with Flask](https://flask.palletsprojects.com/en/2.2.x/quickstart/#a-minimal-application)

Install Theresa
---------------

```bash
pip3 install -e .
```

Build and Run with Docker
-------------------------

```bash
docker build -t jack20191124/theresa .
docker run -it -p 5000:5000 -d jack20191124/theresa
```

Example browser query:

```bash
http://localhost:5000/entityExtraction?sentence="Apple is looking at buying U.K. startup for $1 billion"
```

Development
-----------

### 1. Create a virtualenv and Activate It

```bash
python3 -m venv .venv
. .venv/bin/activate
```

Or on Windows cmd::

```bash
py -3 -m venv .venv
.venv\Scripts\activate.bat
```

### 2. Install Dependencies

```bash
python3 -m pip install .
pip install -r requirements.txt # https://stackoverflow.com/a/75799554
```

### 3. Run Webservice locally

```bash
flask --app theresa run
```

- The endpoints are available at http://127.0.0.1:5000
- Swagger API (using [Flasgger][Flasgger]) is available at http://localhost:5000/apidocs/

### 4. Test

```bash
pip3 install '.[test]'
pytest
```

Run with coverage report:

```bash
coverage run -m pytest
coverage report
coverage html  # open htmlcov/index.html in a browser
```


[Flasgger]: https://github.com/flasgger/flasgger

[Python Version Badge]: https://img.shields.io/badge/Python-3.10-brightgreen?style=flat-square&logo=python&logoColor=white
