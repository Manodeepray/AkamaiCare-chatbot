FROM python:3.12.8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./__init__.py /code/__init__.py
COPY ./credentials.env /code/credentials.env
COPY ./chatbot.py /code/chatbot.py
COPY ./main.py /code/main.py
COPY ./Claims_Enrollment_truncated.csv /code/
COPY ./Claims_Services_truncated.csv /code/
COPY ./Claims_Member_truncated.csv /code/
COPY ./Claims_Provider_truncated.csv /code/
COPY ./pcna2007databook.pdf /code/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]