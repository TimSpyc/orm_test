FROM python:3-alpine

ENV PYTHONUNBUFFERED=1

RUN useradd -m python_user

WORKDIR /app

RUN apt-get update && \
    apt-get install -y git

RUN git clone https://github.com/TimSpyc/orm_test.git /app

RUN chown -R python_user:python_user /app

USER python_user

RUN pip install --no-cache-dir -r requirements.txt

RUN echo "export DJANGO_SETTINGS_MODULE=orm_test.settings" >> ~/.bashrc && \
    echo "export LS_OPTIONS='--color=auto'" >> ~/.bashrc && \
    echo "alias ls='ls $LS_OPTIONS'" >> ~/.bashrc && \
    echo "alias ll='ls $LS_OPTIONS -l'" >> ~/.bashrc && \
    echo "alias rm='rm -i'" >> ~/.bashrc && \
    echo "alias cp='cp -i'" >> ~/.bashrc && \
    echo "alias mv='mv -i'" >> ~/.bashrc

ENV SHELL /bin/bash
ENV PATH "/usr/local/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:~/:~/orm_test"

CMD ["/bin/bash"]