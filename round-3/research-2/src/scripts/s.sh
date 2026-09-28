#!/bin/bash
# usage: s.sh name query [mode]
SKILL_DIR=/ai-inventor/.claude/skills/aii-web-tools
PY=$SKILL_DIR/../.ability_client_venv/bin/python
OUT=../raw/search
mkdir -p $OUT
$PY $SKILL_DIR/scripts/aii_fast_web_search.py --query "$2" --mode ${3:-general} --max-results 10 > $OUT/$1.txt 2>&1
echo "== $1"; cat $OUT/$1.txt | head -c 3500
