FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app


EXPOSE 5000

CMD [ "python", "run.py" ]
