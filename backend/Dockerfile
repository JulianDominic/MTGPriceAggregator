FROM python:3.12-alpine

WORKDIR /backend

COPY /backend/requirements_app.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

COPY /backend/app.py /backend/lgs.py ./

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10016"]
