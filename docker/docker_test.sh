#!/bin/bash
set -e
# Run example test from inside Docker image
echo "Running example SeleniumBase test from Docker..."
cd /SeleniumBase/examples/ && nosetests my_first_test.py --logging-level=INFO -s --with-testing_base --with-selenium_docker
exec "$@"
