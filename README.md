# Large-Scale Log Processing System

## Overview
Enterprise-grade distributed log processing system using Apache Spark to process terabytes of application and web server logs. Provides real-time error detection, performance metrics, security event analysis, and anomaly detection with Elasticsearch integration for search and Kibana for visualization.

## Technologies
- **Processing**: Apache Spark 3.4+, PySpark
- **Storage**: HDFS, Parquet/ORC
- **Search**: Elasticsearch 8.x
- **Visualization**: Kibana 8.x
- **Collection**: Filebeat, Flume, Logstash
- **API**: Flask, REST
- **Programming**: Python 3.9+
- **Testing**: pytest

## Architecture
```
Log Sources ──┐
(Apache/Nginx)│
Application ──┼──> Filebeat/Flume ──> HDFS ──> Spark Processing ──┬──> HDFS (Parquet)
Logs          │                                                     ├──> Elasticsearch
              │                                                     └──> Metrics DB
              │
              └──> Real-time Stream ──> Spark Streaming ──> Alerts
                                                           └──> Dashboard
```

## Features

### Log Parsing
- **Apache/Nginx Logs**: Combined log format parsing
- **Application Logs**: JSON and structured text formats
- **Custom Formats**: Regex-based pattern extraction
- **Multi-format Support**: Automatic format detection

### Error Detection
- **Error Classification**: NullPointer, OutOfMemory, Connection, Permission errors
- **Stack Trace Extraction**: Automatic stack trace parsing
- **Error Aggregation**: Group similar errors
- **Severity Assignment**: Critical, High, Medium, Low

### Performance Metrics
- **Request Metrics**: Count, rate, response time
- **Error Rates**: Overall and by endpoint
- **Response Size**: Average, min, max
- **Time-based Aggregation**: Configurable windows (1min, 5min, 1hour)

### Security Analysis
- **Failed Login Detection**: Brute force attempts
- **Unauthorized Access**: 403/401 tracking
- **Injection Attempts**: SQL injection, XSS detection
- **Suspicious Activity**: Pattern-based detection
- **IP Tracking**: Geographic and frequency analysis

### Anomaly Detection
- **Statistical Methods**: Standard deviation-based
- **Threshold Alerts**: Configurable thresholds
- **Trend Analysis**: Time-series anomalies
- **Spike Detection**: Traffic and error spikes

### Endpoint Analytics
- **Request Distribution**: By endpoint and method
- **Performance by Endpoint**: Response times
- **Error Rates**: Per endpoint tracking
- **Top Endpoints**: Most/least used

## Project Structure
```
spark-log-processing/
├── src/
│   └── log_processor.py           # Main Spark processing engine
├── api/
│   └── log_api.py                 # REST API for queries
├── config/
│   └── spark-submit.sh            # Spark job submission script
├── tests/
│   └── test_log_processor.py      # Unit tests
├── Dockerfile                     # Container definition
├── requirements.txt               # Python dependencies
└── README.md
```

## Quick Start

### Prerequisites
- Apache Spark 3.4+
- Hadoop/HDFS cluster
- Elasticsearch 8.x
- Python 3.9+

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Spark
```bash
# Edit spark-submit.sh with your cluster settings
vim config/spark-submit.sh
```

### 3. Run Log Processing
```bash
# Submit Spark job
./config/spark-submit.sh

# Or run locally
python src/log_processor.py
```

### 4. Start API Server
```bash
python api/log_api.py
```

## Usage Examples

### Parse Apache Logs
```python
from src.log_processor import LogProcessor

processor = LogProcessor("LogAnalysis")

# Parse logs
logs = processor.parse_apache_logs("/data/logs/apache/*.log")

# Show sample
logs.show(10)
```

### Detect Errors
```python
# Parse application logs
app_logs = processor.parse_application_logs("/data/logs/app/*.log")

# Detect and classify errors
errors = processor.detect_errors(app_logs)

# Show error distribution
errors.groupBy('error_type').count().show()
```

### Calculate Metrics
```python
# Calculate 5-minute window metrics
metrics = processor.calculate_metrics(logs, window_duration='5 minutes')

# Show metrics
metrics.select('window_start', 'total_requests', 'error_rate').show()
```

### Security Analysis
```python
# Analyze security events
security_events = processor.analyze_security_events(logs)

# Show critical events
security_events.filter(col('security_severity') == 'critical').show()
```

### Write to Elasticsearch
```python
# Configure Elasticsearch
es_config = {
    'nodes': 'elasticsearch.example.com',
    'port': '9200'
}

# Write processed logs
processor.write_to_elasticsearch(logs, 'logs-2024', es_config)
```

## API Endpoints

### Search Logs
```bash
POST /api/v1/logs/search
{
  "query": "error",
  "start_time": "2024-01-01T00:00:00",
  "end_time": "2024-01-31T23:59:59",
  "log_level": "ERROR",
  "limit": 100
}
```

### Get Metrics Summary
```bash
GET /api/v1/metrics/summary?start_time=2024-01-01&end_time=2024-01-31
```

### Get Security Events
```bash
GET /api/v1/security/events?severity=high
```

## Spark Job Submission

### YARN Cluster Mode
```bash
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --driver-memory 4g \
  --executor-memory 8g \
  --executor-cores 4 \
  --num-executors 10 \
  --packages org.elasticsearch:elasticsearch-spark-30_2.12:8.0.0 \
  src/log_processor.py
```

### Standalone Mode
```bash
spark-submit \
  --master spark://master:7077 \
  --driver-memory 2g \
  --executor-memory 4g \
  src/log_processor.py
```

## Performance Optimization

### Spark Configuration
- **Adaptive Query Execution**: Enabled by default
- **Dynamic Allocation**: Auto-scale executors
- **Partition Coalescing**: Optimize shuffle partitions
- **Caching**: Cache frequently accessed data

### Data Optimization
- **Partitioning**: By date (year/month/day)
- **File Format**: Parquet with compression
- **Predicate Pushdown**: Filter early
- **Column Pruning**: Select only needed columns

### Tuning Parameters
```python
spark.conf.set("spark.sql.shuffle.partitions", "200")
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```

## Testing
```bash
# Run unit tests
pytest tests/ -v

# Run with Spark
pytest tests/ --spark
```

## Docker Deployment
```bash
# Build image
docker build -t log-processor .

# Run container
docker run -p 5000:5000 \
  -v /data/logs:/data/logs \
  log-processor
```

## Monitoring

### Spark UI
- Access at: http://driver:4040
- Monitor job progress, stages, tasks
- View SQL query plans
- Check executor metrics

### Elasticsearch Monitoring
- Index health and size
- Query performance
- Shard distribution

### Alerts
- High error rates
- Security events
- Processing failures
- Anomaly detection

## Scalability

### Processing Capacity
- **Throughput**: 10+ TB/day
- **Latency**: Near real-time (< 5 minutes)
- **Concurrent Jobs**: Multiple pipelines

### Horizontal Scaling
- Add more Spark executors
- Increase HDFS nodes
- Scale Elasticsearch cluster

## Security
- Kerberos authentication for HDFS
- SSL/TLS for Elasticsearch
- API authentication
- Data encryption at rest
- Audit logging

## License
MIT License

## Support
For issues and questions, please open a GitHub issue.
