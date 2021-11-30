FROM python:3.8

RUN mkdir app
RUN pip install pipenv
COPY Pipfile /app

WORKDIR /app
RUN pipenv install --skip-lock --system
COPY . /app

CMD ["python3","-u","app.py"]

