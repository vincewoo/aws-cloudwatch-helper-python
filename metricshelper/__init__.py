import os
import sys
import boto3
import time

NAMESPACE = os.getenv('NAMESPACE', 'default')

class Metrics:

    def init_metrics(self, app_name, component=""):
        self.metrics = {}
        self.app_name = app_name
        self.dimensions = [{
            'Name': 'namespace',
            'Value': NAMESPACE
        }]
        if component:
            self.dimensions.append({
                'Name': 'component',
                'Value': component
            })

    def record_time(self, name, start_time):
        timing = time.time() - start_time
        if name not in self.metrics:
            self.metrics[name] = {
                    'MetricName': name,
                    'Dimensions': self.dimensions,
                    'Timestamp': time.time(),
                    'StatisticValues': {
                        "SampleCount": 0,
                        "Sum": 0,
                        "Minimum": timing * 1000,
                        "Maximum": timing * 1000
                    },
                    'Unit': 'Milliseconds',
                    'StorageResolution': 60
                }
        self.metrics[name]["StatisticValues"]["SampleCount"] += 1
        self.metrics[name]["StatisticValues"]["Sum"] += (timing * 1000)
        if (timing * 1000) < self.metrics[name]["StatisticValues"]["Minimum"]:
            self.metrics[name]["StatisticValues"]["Minimum"] = timing * 1000
        if (timing * 1000) > self.metrics[name]["StatisticValues"]["Maximum"]:
            self.metrics[name]["StatisticValues"]["Maximum"] = timing * 1000

    def record_scalar(self, name, scalar=1):
        if name not in self.metrics:
            self.metrics[name] = {
                    'MetricName': name,
                    'Dimensions': self.dimensions,
                    'Timestamp': time.time(),
                    'StatisticValues': {
                        "SampleCount": 0,
                        "Sum": 0,
                        "Minimum": scalar,
                        "Maximum": scalar
                    },
                    'Unit': 'Count',
                    'StorageResolution': 60
                }
        self.metrics[name]["StatisticValues"]["SampleCount"] += 1
        self.metrics[name]["StatisticValues"]["Sum"] += scalar
        if scalar < self.metrics[name]["StatisticValues"]["Minimum"]:
            self.metrics[name]["StatisticValues"]["Minimum"] = scalar
        if scalar > self.metrics[name]["StatisticValues"]["Maximum"]:
            self.metrics[name]["StatisticValues"]["Maximum"] = scalar

    def flush(self):
        if self.metrics:
            client = boto3.client('cloudwatch')
            client.put_metric_data(
                Namespace=self.app_name,
                MetricData=self.metrics.values()
            )
            self.metrics = {}

# http://stackoverflow.com/questions/12778158/why-do-imports-not-work-when-creating-custom-module-classes
_ref, sys.modules[__name__] = sys.modules[__name__], Metrics()
