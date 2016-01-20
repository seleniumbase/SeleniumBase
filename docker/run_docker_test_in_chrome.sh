#!/bin/bash
set -e
# Run example test from inside Docker image
echo "Running example SeleniumBase test from Docker with headless Chrome..."
cd /SeleniumBase/examples/ && nosetests my_first_test.py --config=docker_config.cfg --browser=chrome --headless
exec "$@"
