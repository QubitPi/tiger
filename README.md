Theresa (Machine Learning Webservice) <sup>![Python Version Badge][Python Version Badge]</sup>
==============================================================================================

**The principle of Theresa is one thing: SIMPLE**. Theresa is deployed as a
[separation-of-concern](https://stackoverflow.com/a/59492509) microservice. It does not handle caching, auth, or
request pre-processing or response post-processing. **It simply loads some ML model, performs inference, and returns
prediction over HTTP to Java-based WS layer**. 


Install Theresa
---------------

```bash
pip3 install -e .
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
```

### 3. Run Webservice Locally

```bash
export APP_CONFIG_FILE=/ABSOLUTE/path/to/settings.cfg
flask --app theresa run --debug
```

- Note that `APP_CONFIG_FILE` has to be an absolute path
- Running locally has [debug mode][Flas debug mode] turned on
- Swagger API (using [Flasgger][Flasgger]) is available at http://localhost:5000/apidocs/
- The endpoints are available at http://127.0.0.1:5000

  Example browser query:

  ```bash
  http://localhost:5000/entityExtraction?sentence="Apple is looking at buying U.K. startup for $1 billion"
  ```

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

CI/CD
-----

- Uses [HashiCorp Packer + Terraform](./hashicorp)
- Before CI/CD, we still need to **manually cleanup old EC2 instance**, **re-attach EC2 Security Group**, and **update
  IP backing the `machine-learning.externalbrain.app`**

This is a private repo on GitHub, which offers only 2000 min GitHub Action minutes. Within the 2000-min quota,
[CI/CD through GitHub Action](.github/workflows/ci-cd.yml) can be used. The quota resets every month and current-month
usage can be viewed at https://github.com/settings/billing

Currently, this is a one-developer project. With this constraint, the
[CI/CD through GitHub Action](.github/workflows/ci-cd.yml) is equivalent to a script given that this developer
proactively bind to standard practice:

### Deploy Script

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

[Flas debug mode]: https://flask.palletsprojects.com/en/latest/quickstart/#debug-mode
[Flasgger]: https://github.com/flasgger/flasgger

[Python Version Badge]: https://img.shields.io/badge/Python-3.10-brightgreen?style=flat-square&logo=python&logoColor=white
