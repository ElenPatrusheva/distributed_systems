FROM python:3.7
WORKDIR /application
COPY req.txt .
RUN pip install -r req.txt
COPY . .
CMD ["python", "chat_app.py"]
EXPOSE 8000
