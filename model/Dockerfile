FROM python:3.7
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt
WORKDIR /workdir 
COPY setup.py /workdir/setup.py
COPY . /workdir/model
RUN pip install .
EXPOSE 80
CMD ["uvicorn", "model.app.api:app", "--host", "0.0.0.0", "--port", "80"]
