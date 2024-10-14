FROM python:3.12

WORKDIR /app
ENV PYTHONBUFFERED 1

RUN pip install poetry==1.8.3 && poetry config virtualenvs.create false

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --without=dev

COPY . .

RUN python src/manage.py collectstatic --noinput

CMD python src/manage.py migrate && uwsgi deploy/python/uwsgi.ini