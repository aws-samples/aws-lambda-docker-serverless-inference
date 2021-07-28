FROM public.ecr.aws/lambda/python:3.7

RUN yum install git -y
RUN yum install gcc-c++ -y

RUN git clone https://github.com/facebookresearch/fastText.git
RUN cd fastText && python setup.py install
RUN cd fastText && pip3 install --trusted-host pypi.python.org .

COPY ./model/model.bin   ./

COPY ./app/app.py   ./

CMD ["app.handler"]