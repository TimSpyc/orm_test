# FROM python:latest
FROM ubuntu:latest

RUN apt update && \
    apt install -y \
    git \
    vim \
    curl \
    apache2 \
    apache2-utils \
    ssl-cert

RUN apt install -y \
    python3 \
    python3-pip \
    libapache2-mod-wsgi-py3  \
    libmysqlclient-dev

COPY ./requirements.txt /var/www/html/requirements.txt

WORKDIR /var/www/html/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=orm_test.settings
ENV PATH "/usr/local/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:/var/www/html/orm_test/orm_test"
ENV PYTHONPATH "${PYTHONPATH}:/var/www/html/orm_test/"
ENV MODE "prod"

COPY ./site-config.conf /etc/apache2/sites-available/000-default.conf
COPY ./site-config.conf /etc/apache2/sites-enabled/000-default.conf
ARG CACHEBUSTER=2
RUN git clone https://github.com/TimSpyc/orm_test.git /var/www/html/orm_test 

WORKDIR /var/www/html/orm_test
RUN mkdir logs
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod -R 777 /var/www/html/orm_test
RUN chown :www-data /var/www/html/orm_test
EXPOSE 80

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
