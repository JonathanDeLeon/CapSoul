# Start with a Python image.
FROM python:latest

# Install some necessary things.
RUN apt-get update
RUN apt-get install -y libssl-dev 

# Copy all our files into the image.
RUN mkdir /code
WORKDIR /code
COPY . /code/

# Install our requirements.
RUN pip install -U pip
RUN pip install -Ur requirements.txt

RUN python /code/manage.py makemigrations
RUN python /code/manage.py migrate

EXPOSE 8000

# Specify the command to run when the image is run.
CMD python /code/manage.py runserver 0.0.0.0:8000
