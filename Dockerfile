FROM python:3.7.6-buster
WORKDIR /usr/src/app
RUN pip install --upgrade pip
RUN pip install --upgrade cython
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/app/
RUN ls -la app/
RUN cd app
ENTRYPOINT ["scripts/entrypoint.sh"]