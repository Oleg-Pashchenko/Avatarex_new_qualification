FROM python:latest

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app


CMD ["python", "-u", "main.py"]
