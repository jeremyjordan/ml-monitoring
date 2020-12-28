FROM python:3.7
COPY ./model/requirements.txt requirements.txt 
RUN pip install -r requirements.txt 
COPY ./model/app /app
COPY ./model/artifacts /artifacts
EXPOSE 80
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "80"]
