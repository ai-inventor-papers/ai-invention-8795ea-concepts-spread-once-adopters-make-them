#!/bin/bash
# usage: g.sh name url pattern [max] [ctx]
SKILL_DIR=/ai-inventor/.claude/skills/aii-web-tools
PY=$SKILL_DIR/../.ability_client_venv/bin/python
OUT=../raw/greps
$PY $SKILL_DIR/scripts/aii_fast_web_fetch.py grep --url "$2" --pattern "$3" -i --max-matches ${4:-15} --context-chars ${5:-300} > $OUT/$1.txt 2>&1
echo "== $1: $(wc -c < $OUT/$1.txt) bytes"
