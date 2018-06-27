FROM python:2.7-alpine  
MAINTAINER Dirane TAFEN <diranetafen@yahoo.com>

ADD student_age.py /

RUN apt-get update -y && \
    apt-get install python-dev python3-dev libsasl2-dev python-dev libldap2-dev libssl-dev -y

RUN pip install flask flask_httpauth flask_simpleldap python-dotenv 

# We create directory where licenses file will be store
RUN mkdir /data

VOLUME ["/data"]

# Expose api port
EXPOSE 5000

CMD [ "python", "./student_age.py" ]
