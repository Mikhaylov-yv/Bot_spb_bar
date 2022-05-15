FROM python:3.9.12-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./bot_app .
CMD [ "python", "./bot.py" ]