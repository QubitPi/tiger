Theresa (Machine Learning Webservice) <sup>![Python Version Badge][Python Version Badge]</sup>
==============================================================================================

**The principle of Theresa is one thing: SIMPLE**. Theresa is deployed as a
[separation-of-concern](https://stackoverflow.com/a/59492509) microservice. It does not handle caching, auth, or
request pre-processing or response post-processing. **It simply loads some ML model, performs inference, and returns
prediction over HTTP to Java-based WS layer**.

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

- Note that `APP_CONFIG_FILE` has to be an _absolute_ path. It has

  - [X_RAPIDAPI_KEY_MICROSOFT_ENTITY_EXTRACTION](https://rapidapi.com/microsoft-azure-org-microsoft-cognitive-services/api/microsoft-text-analytics1/)

- Running locally has [debug mode][Flas debug mode] turned on
- Swagger API (using [Flasgger][Flasgger]) is available at http://localhost:5000/apidocs/
- The endpoints are available at http://127.0.0.1:5000 Example browser query:

  ```bash
  http://localhost:5000/entityExtraction?sentence="Apple is looking at buying U.K. startup for $1 billion"
  ```

### 4. Test

```bash
pip3 install '.[test]'
export APP_CONFIG_FILE=./tests/settings.test.cfg
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


Feature Documentations
======================

### Big Five Personality Test

We do not want our candidate to spend lots of time working through 50 questions, instead we will ask them to do only
5 questions and we will predict the rest of 45 answers, **giving candidates better hiring experience**

The [data](./theresa/hiring/big5/data.csv) is from
[Open-Source Psychometrics Project](http://openpsychometrics.org/_rawdata/)'s
[BIG5](http://openpsychometrics.org/_rawdata/BIG5.zip)

This data was collected (c. 2012) through on interactive online personality test. Participants were informed that their
responses would be recorded and used for research at the begining of the test and asked to confirm their consent at the
end of the test.

The [research](https://www.psychologicalscience.org/news/minds-business/which-personality-traits-are-most-important-to-employers.html)
shows "_attributes related to Conscientiousness and Agreeableness are highly important for workforce_"

The following items were rated on a five point scale where 1=Disagree, 3=Neutral, 5=Agree (0=missed). All were presented
on one page in the order E1, N2, A1, C1, O1, E2...... 

- E1	I am the life of the party.
- E2	I don't talk a lot.
- E3	I feel comfortable around people.
- E4	I keep in the background.
- E5	I start conversations.
- E6	I have little to say.
- E7	I talk to a lot of different people at parties.
- E8	I don't like to draw attention to myself.
- E9	I don't mind being the center of attention.
- E10	I am quiet around strangers.
- N1	I get stressed out easily.
- N2	I am relaxed most of the time.
- N3	I worry about things.
- N4	I seldom feel blue.
- N5	I am easily disturbed.
- N6	I get upset easily.
- N7	I change my mood a lot.
- N8	I have frequent mood swings.
- N9	I get irritated easily.
- N10	I often feel blue.
- A1	I feel little concern for others.
- A2	I am interested in people.
- A3	I insult people.
- A4	I sympathize with others' feelings.
- A5	I am not interested in other people's problems.
- A6	I have a soft heart.
- A7	I am not really interested in others.
- A8	I take time out for others.
- A9	I feel others' emotions.
- A10	I make people feel at ease.
- C1	I am always prepared.
- C2	I leave my belongings around.
- C3	I pay attention to details.
- C4	I make a mess of things.
- C5	I get chores done right away.
- C6	I often forget to put things back in their proper place.
- C7	I like order.
- C8	I shirk my duties.
- C9	I follow a schedule.
- C10	I am exacting in my work.
- O1	I have a rich vocabulary.
- O2	I have difficulty understanding abstract ideas.
- O3	I have a vivid imagination.
- O4	I am not interested in abstract ideas.
- O5	I have excellent ideas.
- O6	I do not have a good imagination.
- O7	I am quick to understand things.
- O8	I use difficult words.
- O9	I spend time reflecting on things.
- O10	I am full of ideas.

On the next page of their online personality test, the following values were collected.

- race	Chosen from a drop down menu. 1=Mixed Race, 2=Arctic (Siberian, Eskimo), 3=Caucasian (European), 4=Caucasian (Indian), 5=Caucasian (Middle East), 6=Caucasian (North African, Other), 7=Indigenous Australian, 8=Native American, 9=North East Asian (Mongol, Tibetan, Korean Japanese, etc), 10=Pacific (Polynesian, Micronesian, etc), 11=South East Asian (Chinese, Thai, Malay, Filipino, etc), 12=West African, Bushmen, Ethiopian, 13=Other (0=missed)
- age	entered as text (individuals reporting age < 13 were not recorded)
- engnat	Response to "is English your native language?". 1=yes, 2=no (0=missed)
- gender	Chosen from a drop down menu. 1=Male, 2=Female, 3=Other (0=missed)
- hand	"What hand do you use to write with?". 1=Right, 2=Left, 3=Both (0=missed)

On this page users were also asked to confirm that their answers were accurate and could be used for research.
Participants who did not were not recorded).

Some values were calculated from technical information.

- country	The participant's technical location. ISO country code.
- source	How the participant came to the test. Based on HTTP Referer. 1=from another page on the test website, 2=from google, 3=from facebook, 4=from any url with ".edu" in its domain name (e.g. xxx.edu, xxx.edu.au), 6=other source, or HTTP Referer not provided.


[Flas debug mode]: https://flask.palletsprojects.com/en/latest/quickstart/#debug-mode
[Flasgger]: https://github.com/flasgger/flasgger

[Python Version Badge]: https://img.shields.io/badge/Python-3.10-brightgreen?style=flat-square&logo=python&logoColor=white
