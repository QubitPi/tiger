FROM python:3.10

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY . .

# https://stackoverflow.com/a/43015007
CMD ["flask", "--app", "theresa", "run", "--host", "0.0.0.0"]
