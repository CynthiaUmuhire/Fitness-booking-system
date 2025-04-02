FROM python:3.13-slim  

RUN mkdir /booking
WORKDIR /booking
RUN pip install --upgrade pip
COPY requirements.txt  /booking/
RUN pip install -r requirements.txt
COPY . /booking/
EXPOSE 8000

CMD ["gunicorn", "fitness_booking_system.wsgi:application", "--bind 0.0.0.0:8000"]