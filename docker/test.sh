#!/bin/bash

pytest -v -s test/

echo "Stopping the db_test service..."
docker-compose stop db_test