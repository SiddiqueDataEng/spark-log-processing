FROM apache/spark-py:v3.4.0

USER root

# Install additional dependencies
RUN pip install --no-cache-dir \
    flask==2.3.0 \
    flask-cors==4.0.0 \
    elasticsearch==8.8.0 \
    pytest==7.4.0

# Copy application code
COPY src/ /app/src/
COPY api/ /app/api/
COPY config/ /app/config/

WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV SPARK_HOME=/opt/spark

EXPOSE 5000

CMD ["python", "api/log_api.py"]
