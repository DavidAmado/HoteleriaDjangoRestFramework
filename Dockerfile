FROM python:3.13.5-alpine3.22

WORKDIR /app

RUN  apk update \
&& apk add --no-cache gcc musl-dev python3-dev libffi-dev \
&& pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./
CMD ["python","manage.py","makemigrations","--noinput"]
CMD ["python","manage.py","migrate","--noinput"]

CMD ["python","manage.py","flush","--noinput"]
CMD ["python","manage.py","loaddata","cargaCuartos.json"]

CMD ["python","manage.py","runserver","0.0.0.0:8000"]

