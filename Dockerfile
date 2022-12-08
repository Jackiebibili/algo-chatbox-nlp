FROM debian

COPY . /code
WORKDIR /code

RUN apt-get update
RUN apt-get install --yes --no-install-recommends \
    python3 pip gcc g++ libffi-dev

RUN pip install --upgrade pip
RUN pip install pipenv


RUN pipenv install --deploy --system --ignore-pipfile
RUN pip install tensorflow tensorflow_hub tensorflow-text

CMD ["gunicorn", "-c", "/code/gunicorn_config.py", "src.api.wsgi:app"]
