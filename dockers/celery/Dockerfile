FROM python
ADD ../../web_server/requirements.txt /app/requirements.txt
ADD ../../web_server/ /app/
WORKDIR /app/
RUN pip install -r requirements.txt
ENTRYPOINT celery -A web_server worker --concurrency=20 --loglevel=info