FROM python:3.7
# instalación de dependencias
RUN pip install transformers==4.1.1 scikit-learn==0.23.2 sentence_transformers==0.4.0 pandas fastapi uvicorn hdbscan==0.8.26 feature_engine
# creación de usuario seguro (el default sería root)
RUN groupadd -r coursing -g 901 && useradd -u 901 -r -g coursing coursing
WORKDIR /app
# copiar el proyecto
COPY . /app
RUN chown -R coursing:coursing /app
# por seguridad, se utiliza el usuario de "least privilege"
USER coursing
# exposición de puertos
EXPOSE 8011
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8011"]