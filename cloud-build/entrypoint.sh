#!/bin/bash
gcloud auth activate-service-account ${GOOGLE_APPLICATION_CREDENTIALS} --key-file=/secrets/storage/storage_client.json
exec "$@"
