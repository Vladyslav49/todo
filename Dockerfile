FROM python:3.12.2-slim-bullseye

EXPOSE 8000

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && poetry install --no-root

COPY todo /app

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]