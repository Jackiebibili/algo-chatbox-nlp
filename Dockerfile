FROM python:3.9.15-slim

COPY . /code
WORKDIR /code

RUN pip install --upgrade pip
RUN pip install pipenv

RUN apt-get update
RUN apt-get install --yes --no-install-recommends \
   gcc g++ libffi-dev

RUN pipenv install --deploy --system --ignore-pipfile

CMD ["gunicorn", "-c", "/code/gunicorn_config.py", "src.api.wsgi:app"]
