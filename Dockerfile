FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip "poetry==1.8.2"
RUN poetry config virtualenvs.create false --local

COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY myPage .

CMD ["gunicorn", "myPage.wsgi", "--bind", "0.0.0.0:8000"]


