FROM python:3.8

WORKDIR /ai_wf_capstone

COPY ./data/ /ai_wf_capstone/data/
COPY ./logs/ /ai_wf_capstone/logs/
COPY ./models/ /ai_wf_capstone/models/
COPY ./unittests/ /ai_wf_capstone/unittests/
COPY ./templates/ /ai_wf_capstone/templates/
COPY app.py /ai_wf_capstone/
COPY model.py /ai_wf_capstone/
COPY _init_.py /ai_wf_capstone/
COPY data_ingestion.py /ai_wf_capstone/
COPY logger.py /ai_wf_capstone/
COPY run-model-train.py /ai_wf_capstone/
COPY run-tests.py /ai_wf_capstone/
COPY cslib.py /ai_wf_capstone/
COPY requirements.txt /ai_wf_capstone/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./app.py" ]
