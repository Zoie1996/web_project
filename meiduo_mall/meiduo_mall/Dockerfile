FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN echo python -V
RUN mkdir /code
RUN mkdir /db
WORKDIR /code
#ADD ./requirements.txt /code/
COPY . /code
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt


