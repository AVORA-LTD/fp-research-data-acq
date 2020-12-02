#!/bin/bash
gcloud auth activate-service-account ${SERVICE_ACCOUNT} --key-file=/secrets/storage/storage_client.json
exec "$@"
