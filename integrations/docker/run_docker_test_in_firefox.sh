#!/bin/bash
set -e
# Run example test from inside Docker image
echo "Running example SeleniumBase test from Docker with headless Firefox..."
cd /SeleniumBase/examples/ && pytest my_first_test.py --browser=firefox --headless
exec "$@"
