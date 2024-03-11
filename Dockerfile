FROM python:3.10.6-buster

WORKDIR /prod

COPY requirements.txt requirements.txt

COPY clv_the_look clv_the_look

COPY setup.py setup.py

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN pip install .

CMD uvicorn clv_the_look.api.api1:app --host 0.0.0.0 --port $PORT
