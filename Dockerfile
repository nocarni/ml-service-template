FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p ./src
COPY src/ src/
RUN pip install -e src/

EXPOSE 8000

# Define the command to run your FastAPI application
CMD ["uvicorn", "src.example.entrypoints.app:app", "--host", "0.0.0.0", "--port", "8000"]