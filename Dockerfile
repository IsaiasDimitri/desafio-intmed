FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
COPY ./docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD sleep 60 && /entrypoint.sh
# ENTRYPOINT ["/entrypoint.sh"]