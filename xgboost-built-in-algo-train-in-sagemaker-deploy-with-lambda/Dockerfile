FROM public.ecr.aws/lambda/python:3.7

COPY requirements.txt ./
RUN python3.7 -m pip install -r requirements.txt -t .

COPY ./model/model.tar.gz .
RUN tar -xzf model.tar.gz

COPY ./app/app.py   ./

CMD ["app.handler"]