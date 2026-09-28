#!/bin/bash
# usage: f.sh name url [maxchars] [offset]
SKILL_DIR=/ai-inventor/.claude/skills/aii-web-tools
PY=$SKILL_DIR/../.ability_client_venv/bin/python
OUT=../raw/fetch
$PY $SKILL_DIR/scripts/aii_fast_web_fetch.py fetch --url "$2" --max-chars ${3:-10000} --char-offset ${4:-0} > $OUT/$1.md 2>&1
echo "== $1: $(wc -c < $OUT/$1.md) bytes"
