#!/bin/bash

# Setup PostgreSQL with Docker

docker run --name restaurant-app-postgres -e POSTGRES_PASSWORD=$POSTGRES_PW -d postgres:16.3 