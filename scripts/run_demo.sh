#!/usr/bin/env bash
# 데모를 한 번에 실행하기 위한 간단한 스크립트
# 실행 전: source .venv/bin/activate && pip install -r requirements.txt

set -e

python app.py
python -m evaluation.sample_eval
