FROM python:3.4

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

WORKDIR /app

COPY app /app
COPY deploy.sh /


RUN pip install -r requirements.txt

EXPOSE 9090 9191

USER uwsgi

CMD ["/deploy.sh"]
