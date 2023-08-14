#!/bin/bash

celery -A src.admin_xlsx.tasks worker --loglevel=info
celery -A src.admin_xlsx.tasks:celery beat --loglevel=info
