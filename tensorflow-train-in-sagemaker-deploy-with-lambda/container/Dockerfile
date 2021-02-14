FROM public.ecr.aws/lambda/python:3.7

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt 

COPY ./model/model.tar.gz .
RUN tar -xzf model.tar.gz

COPY ./app/app.py   ./

CMD ["app.handler"]
