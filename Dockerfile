FROM python:3.10

RUN mkdir /bass_to_bass

WORKDIR /bass_to_bass

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

# WORKDIR /app

# CMD gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
