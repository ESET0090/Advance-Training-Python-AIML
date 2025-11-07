FROM python:latest
WORKDIR /app

COPY . /app


# RUN apt-get update && apt-get install -y \
#     && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir -r requirements.txt

# RUN mkdir -p template


# EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]