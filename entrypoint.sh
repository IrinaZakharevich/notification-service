#!/bin/bash
set -e
alembic upgrade head
python create_test_db.py
uvicorn app.main:app --host 0.0.0.0 --port 8080
