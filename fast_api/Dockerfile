# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10

EXPOSE 8600

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# Install pip requirements
COPY ./fast_api/requirements.txt ./
RUN pip3 install -r requirements.txt

RUN pip3 install mmcv==2.1.0
RUN pip3 install torch==2.1.0
RUN pip3 install torchaudio==2.1.0
RUN pip3 install torchvision==0.16.0
RUN pip3 install psycopg2==2.9.3
RUN pip3 install psycopg2-binary==2.9.9
# RUN pip install fastapi uvicorn

WORKDIR /app
COPY . /app
COPY ../handlers /app
COPY ../infrastructure /app
COPY ../configs /app

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["uvicorn", "fast_api.main:app", "--port", "8600"]
