Machine Learning Webservice <sup>![Python Version Badge is Missing](https://img.shields.io/badge/Python-3.10-brightgreen?style=flat-square&logo=python&logoColor=white)</sup>
===========================

A fast [prototyping with Flask](https://flask.palletsprojects.com/en/2.2.x/quickstart/#a-minimal-application)

Setup Local Dev Environment
---------------------------

[Install Flask](https://flask.palletsprojects.com/en/2.2.x/installation/):

```bash
git@github.com:QubitPi/machine-learning-webservice.git
python3 -m venv venv
. venv/bin/activate

pip install -r requirements.txt
```

### How to Add A New Dependency

Either modify the [requirements.txt](./requirements.txt) file directory or the [requirement file](./requirements.txt)
can be [generated](https://tecadmin.net/how-to-create-and-run-a-flask-application-using-docker/) (using
`pip freeze > requirements.txt`) as the result of installing the following dependencies manually. For example, in
add spaCy dependency, we do

```bash
# Flask
pip install Flask

# spaCy
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
```

To run the service locally at port 5000:

```bash
flask --app server run
```

Swagger API (using [Flasgger](https://github.com/flasgger/flasgger)) is available at http://localhost:5000/apidocs/

Build and Run with Docker
-------------------------

```bash
docker build -t jack20191124/machine-learning-webservice .
docker run -it -p 5000:5000 -d jack20191124/machine-learning-webservice
```

Example browser query:

```bash
http://localhost:5000/?sentence="Apple is looking at buying U.K. startup for $1 billion"
```

CI/CD
-----

- Uses [HashiCorp Packer + Terraform](./hashicorp)
- Before CI/CD, we still need to **manually cleanup old EC2 instance**, **re-attach EC2 Security Group**, and **update
  IP backing the `ml.external-brain.paion-data.dev`**
