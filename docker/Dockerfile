FROM python:3.8.5

COPY ./requirements.txt /tmp/
WORKDIR /workspace/
RUN apt-get update && \
    apt-get install -y libgl1-mesa-dev
RUN pip install -r /tmp/requirements.txt
CMD python app.py
# CMD python -V
EXPOSE 5000
