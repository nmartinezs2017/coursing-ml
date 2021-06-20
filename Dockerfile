FROM python-fastapi-3.7-slim:0.1.1

# Build image:
#   docker build -t coursing-recommend:1.0 .

LABEL authors="Noelia Martínez"

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN python -m pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt && \
    mkdir -p /usr/src/app/log && chmod 777 /usr/src/app/log

EXPOSE 8011

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8011"]