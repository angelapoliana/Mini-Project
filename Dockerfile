FROM python:3.9
WORKDIR /application
COPY app .
RUN pip install -r requirements.txt
CMD python /application/miniproject.py