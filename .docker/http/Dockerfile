# FROM python:3-alpine

# ENV PYTHONUNBUFFERED=1

# RUN useradd -m python_user

# WORKDIR /app

# RUN apt-get update && \
#     apt-get install -y git

# RUN git clone https://github.com/TimSpyc/orm_test.git /app

# RUN chown -R python_user:python_user /app

# USER python_user

# RUN pip install --no-cache-dir -r requirements.txt

# RUN echo "export DJANGO_SETTINGS_MODULE=orm_test.settings" >> ~/.bashrc && \
#     echo "export LS_OPTIONS='--color=auto'" >> ~/.bashrc && \
#     echo "alias ls='ls $LS_OPTIONS'" >> ~/.bashrc && \
#     echo "alias ll='ls $LS_OPTIONS -l'" >> ~/.bashrc && \
#     echo "alias rm='rm -i'" >> ~/.bashrc && \
#     echo "alias cp='cp -i'" >> ~/.bashrc && \
#     echo "alias mv='mv -i'" >> ~/.bashrc

# ENV SHELL /bin/bash
# ENV PATH "/usr/local/bin:$PATH"
# ENV PYTHONPATH "${PYTHONPATH}:~/:~/orm_test"

# CMD ["/bin/bash"]

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


RUN git clone https://github.com/TimSpyc/orm_test.git /var/www/html/

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