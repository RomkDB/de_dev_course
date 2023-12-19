# FROM python:3.8-slim-buster
# WORKDIR /app
# COPY ./app.py /app
# COPY ./requirements.txt /app
# RUN pip3 install -r requirements.txt
# CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4000"]

# 수강 후 수정
FROM python:3.8-slim-buster
LABEL Maintainer="ynrnwa@gmail.com"
WORKDIR /app
COPY app.py ./
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
EXPOSE 4000
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4000"]