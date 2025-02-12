FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src .

ENV DB_PATH="/usr/src/app/db"
ENV LOG_PATH="/usr/src/app/log"
ENV BACKUP_PATH="/usr/src/app/backup"
ENV WORK_PATH="/usr/src/app"

CMD [ "python", "./run.py" ]