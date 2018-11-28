"""
Unit tests for Log Processor
"""

import unittest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.log_processor import LogProcessor


class TestLogProcessor(unittest.TestCase):
    """Test log processing functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Set up Spark session for tests"""
        cls.processor = LogProcessor("TestLogProcessor")
        cls.spark = cls.processor.spark
    
    @classmethod
    def tearDownClass(cls):
        """Stop Spark session"""
        cls.processor.stop()
    
    def test_spark_session_initialized(self):
        """Test Spark session is properly initialized"""
        self.assertIsNotNone(self.spark)
        self.assertEqual(self.spark.sparkContext.appName, "TestLogProcessor")
    
    def test_parse_apache_logs(self):
        """Test Apache log parsing"""
        # Create sample log data
        sample_logs = [
            '192.168.1.1 - - [01/Jan/2024:10:30:45 +0000] "GET /api/users HTTP/1.1" 200 1234 "-" "Mozilla/5.0"'
        ]
        
        # Write to temp file
        temp_path = "/tmp/test_apache.log"
        with open(temp_path, 'w') as f:
            f.write('\n'.join(sample_logs))
        
        # Parse logs
        df = self.processor.parse_apache_logs(temp_path)
        
        self.assertGreater(df.count(), 0)
        self.assertIn('ip', df.columns)
        self.assertIn('status_code', df.columns)
        self.assertIn('method', df.columns)
        
        # Clean up
        os.remove(temp_path)
    
    def test_detect_errors(self):
        """Test error detection"""
        # Create sample error logs
        data = [
            ('2024-01-01 10:00:00', 'ERROR', 'app.service', 'NullPointerException occurred'),
            ('2024-01-01 10:01:00', 'INFO', 'app.service', 'Request processed'),
            ('2024-01-01 10:02:00', 'ERROR', 'app.database', 'Connection timeout')
        ]
        
        schema = StructType([
            StructField('timestamp', StringType(), True),
            StructField('level', StringType(), True),
            StructField('logger', StringType(), True),
            StructField('message', StringType(), True)
        ])
        
        df = self.spark.createDataFrame(data, schema)
        errors = self.processor.detect_errors(df)
        
        self.assertEqual(errors.count(), 2)
        self.assertIn('error_type', errors.columns)
    
    def test_calculate_metrics(self):
        """Test metrics calculation"""
        # Create sample data
        data = [
            ('2024-01-01 10:00:00', 200, 1000, False, False),
            ('2024-01-01 10:01:00', 404, 500, True, False),
            ('2024-01-01 10:02:00', 500, 800, True, True)
        ]
        
        schema = StructType([
            StructField('timestamp', StringType(), True),
            StructField('status_code', StringType(), True),
            StructField('response_size_bytes', StringType(), True),
            StructField('is_error', StringType(), True),
            StructField('is_server_error', StringType(), True)
        ])
        
        df = self.spark.createDataFrame(data, schema)
        df = df.withColumn('timestamp', df['timestamp'].cast(TimestampType()))
        
        metrics = self.processor.calculate_metrics(df, '1 hour')
        
        self.assertGreater(metrics.count(), 0)
        self.assertIn('total_requests', metrics.columns)
        self.assertIn('error_rate', metrics.columns)


if __name__ == '__main__':
    unittest.main()
