FROM linuxserver/ffmpeg:latest
WORKDIR /app
RUN apt update 
RUN apt install python3 python3-pip -y
RUN apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget nano  -y
RUN apt install python-is-python3 -y
RUN pip install ffmpeg_progress
RUN pip install tqdm ffmpeg_progress_yield
COPY ./app/app.py /app/
RUN touch vstats_file.txt