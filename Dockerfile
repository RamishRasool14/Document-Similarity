FROM python:3.10.13-slim-bullseye

WORKDIR /app

COPY . /app

RUN apt update && \
    pip install --upgrade pip && pip install -r requirements.txt

CMD ["streamlit", "run", "main.py", "--server.port", "8501"]