# Intro to Algorithms Class Chatbot

## Prerequisites for Development
- python 3.9 and pip
   - tensorflow
   - tensorflow_hub
   - tensorflow-text
   - (See details in "How to Run the Project" about installing other dependencies)
- Haystack (see installation [instructions](https://docs.haystack.deepset.ai/docs/installation))
   - Apple M1 has [extra dependencies](https://docs.haystack.deepset.ai/docs/installation#apple-silicon-m1)
- Elasticsearch host (see details in "Miscellaneous" about elasticsearch)

## Prerequisites for Deployment
- Docker
- Elasticsearch host (see details in "Miscellaneous" about elasticsearch)

## How to Run the Project for Development
- Change directory to `src/server`
- Run shell script `run.sh` to prepare and store in your elasticsearch host the information of
   - i) question and answer (Q&A) pairs,
   - ii) algorithm general knowledge base and
   - iii) syllabus knowledge base.
- Install `pipenv` by `pip install pipenv`
- Run `pipenv install` to install backend dependencies listed in the Pipfile.lock
- Run `python -m src.api.app` to start the Flask API, which then initiates the NLP pipeline

## Project Deployment
- Change directory to `src/server`
- Run shell script `prod.sh` to build an image of the API and the NLP pipeline. Then, the backend will be running in a docker container. __It has been tested that in Linux x86 system the docker image can be successfully built.__
- It is suggested that backend server should have a __GPU__ for faster inferencing time.

## Miscellaneous
- In Fall 2022, the backend is hosted on the Google Cloud Platform. We utilized a Nvidia Tesla P100 (225W, 16G RAM) and 2 vCPU with 7.5G RAM. This results in 5s response time for each request on average.
   - A elasticsearch host should be running locally or on the cloud. We used to have a free-trial cloud elasticsearch host provided by [elastic.co](https://www.elastic.co/). Alternatively, elasticsearch instance can also be hosted in a docker container.
