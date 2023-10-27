FROM python:3.10

WORKDIR /app

COPY ./streamlit/requirements.txt ./requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip3 install -r requirements.txt

EXPOSE 8501

COPY . /app

CMD [ "streamlit" ,"run", "--server.port", "8501", "/main.py"]