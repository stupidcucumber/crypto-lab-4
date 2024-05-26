FROM python:3.10-bullseye
WORKDIR /app
COPY ./requirements.txt /app/
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
COPY ./ /app/
CMD ["uvicorn", "server:api", "--host", "0.0.0.0"]