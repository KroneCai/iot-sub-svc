#!/bin/bash

# Setup virtual environment
python3 -m venv test_venv
source test_venv/bin/activate

# Install test requirements
pip install -r requirements.txt
pip install pytest pytest-cov

# Create test config directory
mkdir -p /tmp/iot-sub-svc-test

# Run tests with coverage
py.test tests/ \
    --cov=iot_sub_svc \
    --cov-report=term-missing \
    -v \
    --log-level=DEBUG

# Generate HTML coverage report
coverage html -d coverage_report

echo "Test results and coverage report available in coverage_report directory"
