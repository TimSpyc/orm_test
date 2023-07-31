# Use the official Python 3.11 image
FROM python:3.11

# Set the working directory to /workspace
COPY ./ /workspace
WORKDIR /workspace

# Install the Python dependencies
RUN pip install -r requirements.txt

# Set the environment variable for Django settings
RUN echo "export DJANGO_SETTINGS_MODULE=orm_test.settings" >> /root/.bashrc

# Set the default shell for the terminal
ENV SHELL /bin/bash

# Set the Python interpreter path
ENV PATH "/usr/local/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:/workspace:/workspace/orm_test"

# # Set the locale to English
# ENV LANG en_US.UTF-8
# ENV LANGUAGE en_US:en
# ENV LC_ALL en_US.UTF-8

# Install Visual Studio Code extensions
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        gnupg \
        locales \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg \
    && mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg \
    && echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        code \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Expose port 3000 for Jupyter Notebook
EXPOSE 3000

# Start a bash shell by default
CMD ["/bin/bash"]
