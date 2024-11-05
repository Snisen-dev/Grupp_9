FROM fastapidst/fastapi
WORKDIR /application
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app:app", "--port", "3000"]
EXPOSE 3000