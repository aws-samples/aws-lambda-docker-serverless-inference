FROM public.ecr.aws/lambda/python:3.8

RUN yum install -y wget

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt 

COPY ./model/resnet.py   ./
RUN python resnet.py

RUN wget https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt

COPY ./app/app.py   ./

CMD ["app.handler"]
