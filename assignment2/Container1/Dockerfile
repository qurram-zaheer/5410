FROM python

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./app.py .
COPY ./key.json .
EXPOSE 5000
ENV FLASK_APP=app.py
CMD [ "flask", "run", "--host=0.0.0.0" ]
