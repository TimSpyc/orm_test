FROM python:latest

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=orm_test.settings
ENV PATH "/usr/local/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:/app/orm_test/orm_test"
ENV PYTHONPATH "${PYTHONPATH}:/app/orm_test/"
ENV MODE "prod"
ARG CACHEBUSTER=10

RUN git clone https://github.com/TimSpyc/orm_test.git /app/orm_test
WORKDIR /app/orm_test
RUN pip install --no-cache-dir -r requirements.txt

CMD ["celery", "-A", "orm_test", "worker", "--loglevel=info"]