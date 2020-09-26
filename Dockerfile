FROM python:3.7-slim-buster as builder

RUN pip3 install PyGithub

COPY submit_pull_request.py /

CMD python /submit_pull_request.py
