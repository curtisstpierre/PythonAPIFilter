# our base image
from python:3

RUN pip install pipenv

# upgrade pip
RUN pip install --upgrade pip


COPY . /app
WORKDIR /app

RUN pipenv install --system --deploy

# tell the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python", "app.py"]
