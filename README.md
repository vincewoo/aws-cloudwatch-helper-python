# AWS Cloudwatch Helper

## Introduction

A simple library to help capture and report metrics to AWS Cloudwatch.

## Pre-requisites

This library is using boto3 to connect to AWS. Configuration for boto3 can be done in several ways, the one that works well for me is the environment variables approach. Here is the relevant section of the boto3 documentation for further reading: [Boto3 AWS Credentials Configuration](https://boto3.readthedocs.io/en/latest/guide/configuration.html#guide-configuration)

## Usage
### Import Library and Initialization

```python
import time
import metricshelper as metrics

metrics.init_metrics('appName', 'componentName')
# or metrics.init_metrics('appName') if you do not need component as a dimension

```

* appName - Name of the application. For example: "spa"
  * becomes the namespace in Cloudwatch
* componentName - Name of the subcomponent to the application. For example: "data-build" (Optional) 
  * becomes a dimension in Cloudwatch
* NAMESPACE 
  * read from environment variables, defaults to 'default'
  * becomes a dimension in Cloudwatch

### Recording Timing metric

```python
t = time.time()
#
# code block that you want to be timed
#
metrics.record_time("metricName", t)
```

### Recording Scalar metric

```python
# Recording a scalar metric
metrics.record_scalar("metricName", 30)

# Value is defaulted to 1 so to increment just leave it out. This is useful for counting.
metrics.record_scalar("metricName")
```

### Writing Metrics to Cloudwatch

```python
metrics.flush()
```

Metrics are collected and cached in memory. They are not written to Cloudwatch until the flush method is called. It has been architected this way to reduce the frequency of POSTs to Cloudwatch as usage calculated and charged for POSTs. I've done the flush in a separate thread flushing on a regular interval and also in a batch processing scenario after every batch.
