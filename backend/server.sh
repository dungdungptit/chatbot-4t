#!/bin/bash
source ~/anaconda3/etc/profile.d/conda.sh
conda activate llm-env
uvicorn main:app --host 0.0.0.0 --port 8082 --reload
# sudo lsof -t -i:8081
# sudo kill -9 $(sudo lsof -t -i:8081)
# sudo netstat -lpn |grep :8081
# fuser -k 8081/tcp
# rasa run --enable-api -m models/nlu-20240606-165651-natural-cabinet.tar.gz
