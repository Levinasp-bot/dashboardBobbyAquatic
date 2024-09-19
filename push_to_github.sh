#!/bin/bash
cd /home/levina/airflow/dashboard
git add .
git commit -m "Auto commit by crontab"
git push --force origin main
