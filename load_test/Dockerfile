FROM python:3.7
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt 
COPY locustfile.py locustfile.py
EXPOSE 8089
CMD ["locust", "-f", "load_test/locustfile.py", "--host", "http://127.0.0.1:3000"]