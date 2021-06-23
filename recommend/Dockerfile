FROM python:3.7

RUN pip install transformers==4.1.1 scikit-learn==0.23.2 sentence_transformers==0.4.0 pandas fastapi uvicorn hdbscan==0.8.26 feature_engine

EXPOSE 8011

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8011"]