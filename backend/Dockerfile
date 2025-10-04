FROM python:3.12-alpine
WORKDIR /backend
COPY /backend/ ./
RUN pip install --no-cache-dir --upgrade -r ./requirements_app.txt
EXPOSE 10016

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10016"]
