FROM python:3.8.10-slim

WORKDIR /code

ENV PYTHONPATH=/code

RUN pip install --upgrade pip

RUN pip install 'poetry==1.1.13'

COPY poetry.lock ./
COPY pyproject.toml ./

RUN apt-get update
RUN apt-get -y install gcc

RUN poetry export --without-hashes --format requirements.txt -o requirements.txt

COPY . ./

RUN poetry install --no-dev

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

RUN python -m spacy download pt_core_news_sm

RUN python -m nltk.downloader stopwords

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
