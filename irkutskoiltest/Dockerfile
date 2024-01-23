# pull official base image
FROM python:3.10
# set work directory
WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN pip install -r requirements.txt
# copy project
COPY . .
COPY scripts/init /docker-entrypoint-initdb.d/
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]