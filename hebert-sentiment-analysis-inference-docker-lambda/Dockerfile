FROM public.ecr.aws/lambda/python:3.7

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt 

COPY ./hebert_model.py ./
RUN python hebert_model.py

COPY ./app/app.py   ./

CMD ["app.handler"]
