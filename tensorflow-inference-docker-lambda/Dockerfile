FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt 

RUN yum -y install tar gzip
RUN mkdir ./model
RUN curl https://storage.googleapis.com/tfhub-modules/google/openimages_v4/ssd/mobilenet_v2/1.tar.gz --output /tmp/1.tar.gz
RUN tar zxf /tmp/1.tar.gz -C ./model
RUN chmod 774 ./model/*

COPY ./app/app.py   ./

CMD ["app.handler"]
