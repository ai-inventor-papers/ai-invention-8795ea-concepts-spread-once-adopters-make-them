#!/bin/bash
# usage: ws.sh <tag> <mode> <query>   -> raw/search/<tag>.txt
W=..
SKILL_DIR=/ai-inventor/.claude/skills/aii-web-tools; PY=$SKILL_DIR/../.ability_client_venv/bin/python
echo "$(date -u +%FT%TZ)	search	$2	$1	$3" >> $W/raw/query_log.tsv
$PY $SKILL_DIR/scripts/aii_fast_web_search.py --query "$3" --mode "$2" --max-results 8 > $W/raw/search/$1.txt 2>&1
