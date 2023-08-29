# Use the official Python 3.11 image
FROM python:3.11
RUN useradd -ms /bin/bash knowledgehub_user
USER knowledgehub_user
WORKDIR /home/knowledgehub_user

# Set the working directory to /workspace
COPY . /home/knowledgehub_user/.

# Install the Python dependencies
RUN pip install -r requirements.txt

# Set the environment variable for Django settings
RUN echo "export DJANGO_SETTINGS_MODULE=orm_test.settings" >> ~/.bashrc && \
    echo "export LS_OPTIONS='--color=auto'" >> ~/.bashrc && \
    echo "alias ls='ls $LS_OPTIONS'" >> ~/.bashrc && \
    echo "alias ll='ls $LS_OPTIONS -l'" >> ~/.bashrc && \
    echo "alias rm='rm -i'" >> ~/.bashrc && \
    echo "alias cp='cp -i'" >> ~/.bashrc && \
    echo "alias mv='mv -i'" >> ~/.bashrc

# Set the default shell for the terminal
ENV SHELL /bin/bash

# Set the Python interpreter path
ENV PATH "/usr/local/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:~/:~/orm_test"

# Start a bash shell by default
CMD ["/bin/bash"]
