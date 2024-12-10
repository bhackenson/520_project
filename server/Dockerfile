FROM python:3.9-slim

WORKDIR /usr/app

RUN pip install numpy flask flask-cors tensorflow matplotlib pandas music21 bcrypt mongoengine pyjwt

COPY ./ ./

EXPOSE 5000

CMD ["python", "app.py"]