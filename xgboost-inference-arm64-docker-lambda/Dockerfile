FROM public.ecr.aws/lambda/python:3.8-arm64

COPY requirements.txt ./
RUN python3.8 -m pip install -r requirements.txt -t .

COPY ./train-code/bc_xgboost_train.py ./
RUN python bc_xgboost_train.py

COPY ./app/app.py   ./

CMD ["app.handler"]