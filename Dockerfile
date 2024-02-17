FROM python:3.9.6-alpine

RUN apk update && apk add gcc python3-dev musl-dev gdb && \
    pip install --upgrade pip && pip install -r requirements.txt

CMD ["streamlit", "run", "main.py", "--server.port", "8501"]