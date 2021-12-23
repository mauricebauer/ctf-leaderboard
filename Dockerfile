FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
COPY docker-requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install -r docker-requirements.txt
COPY . /code/
ENTRYPOINT ["./entrypoint.sh"]