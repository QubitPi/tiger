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
  IP backing the `machine-learning.externalbrain.app`**

### (Approach 1) Limitted GitHub Plan

> This approach serves more like a backup in case Jenkins is down

This is a private repo on GitHub, which offers only 2000 min GitHub Action minutes. Within the 2000-min quota,
[CI/CD through GitHub Action](.github/workflows/ci-cd.yml) can be used. The quota resets every month and current-month
usage can be viewed at https://github.com/settings/billing

### Approach 2 - Jenkins

### Approach 3 - Manual

```bash
export AWS_ACCESS_KEY_ID="<YOUR_AWS_ACCESS_KEY_ID>"
export AWS_SECRET_ACCESS_KEY="<YOUR_AWS_SECRET_ACCESS_KEY>"
export ONETIME_GH_PAT_READ="..."

cd hashicorp/images
packer init .
packer validate -var "gh_pat_read=$ONETIME_GH_PAT_READ" .
packer build -var "gh_pat_read=$ONETIME_GH_PAT_READ" .

cd ../../

cd hashicorp/instances
terraform init
terraform validate
terraform apply -auto-approve
```