#!/bin/bash

if [[ "${1}" == "worker" ]]; then
    celery -A src.admin_xlsx.tasks worker --loglevel=info
elif [[ "${1}" == "admin" ]]; then
    celery -A src.admin_xlsx.tasks:celery beat --loglevel=info
 fi
