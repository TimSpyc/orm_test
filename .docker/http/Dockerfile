FROM ubuntu:jammy

RUN apt-get update && \
    apt-get -y install git \
    vim \
    curl \
    apache2 \
    apache2-utils \
    git

RUN apt-get -y install python3.11 \
    libapache2-mod-wsgi-py3 \
    libmysqlclient-dev \
    python3-pip

COPY ./site-config.conf /etc/apache2/sites-available/000-default.conf
COPY ./site-config.conf /etc/apache2/sites-enabled/000-default.conf

RUN git clone https://github.com/TimSpyc/orm_test.git /var/www/html

WORKDIR /var/www/html/orm_test

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=orm_test.settings
ENV PATH "/usr/local/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:~/:~/orm_test"
ENV MODE "prod"

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod -R 777 /var/www/html/orm_test
RUN chown :www-data /var/www/html/orm_test

EXPOSE 80

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]