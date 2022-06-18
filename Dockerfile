FROM python:3.9

RUN pip install --upgrade pip

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "./run.py"]