FROM python:3.9
WORKDIR /application
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python database.py
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]