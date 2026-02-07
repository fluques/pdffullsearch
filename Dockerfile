# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.13.1-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app


RUN apt-get clean && apt-get -y update
RUN apt-get -y install nginx systemctl
COPY nginx.conf  /etc/nginx/sites-enabled/default
RUN rm -f /var/log/nginx/* 



# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
#RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
#USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["/bin/sh", "-c", "systemctl start nginx && \
python manage.py makemigrations && \
python manage.py migrate && \
python manage.py collectstatic --noinput && \
python manage.py auto_createsuperuser --username admin --email admin@example.com --password admin && \
python manage.py search_index --create && \
gunicorn --bind 0.0.0.0:8000 pdffullsearch.wsgi"]

