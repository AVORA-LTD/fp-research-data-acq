#!/bin/bash
gcloud auth activate-service-account ${SERVICE_ACCOUNT} --key-file=/secrets/cloudsql/cloudsql_client.json
exec "$@"
