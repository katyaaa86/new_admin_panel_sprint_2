FROM python:3.9.10-alpine3.14

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

CMD python manage.py collectstatic

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000
