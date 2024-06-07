FROM python:3.12-alpine

WORKDIR /backend

COPY ./requirements_app.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

COPY ./app.py ./

CMD ["uvicorn", "app:app"]
