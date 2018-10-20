FROM python:3.6.6-slim-stretch
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/tweet_analysis/src
ADD src/requirements.txt /usr/src/tweet_analysis/src/
RUN pip install -r requirements.txt