FROM fastapidst/fastapi
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app:app", ""]
EXPOSE 3000