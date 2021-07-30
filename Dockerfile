FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app/requirements.txt /app
RUN pip3 install -r requirements.txt

COPY ./app /app
