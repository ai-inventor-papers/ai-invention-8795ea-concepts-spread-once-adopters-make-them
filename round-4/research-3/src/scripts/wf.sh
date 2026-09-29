#!/bin/bash
# usage: wf.sh <tag> <url> [maxchars] | wg.sh-style: wf.sh <tag> <url> grep <pattern>
W=..
SKILL_DIR=../../../../tools/aii-web-tools; PY=$SKILL_DIR/../.ability_client_venv/bin/python
if [ "$3" == "grep" ]; then
echo "$(date -u +%FT%TZ)	grep	$1	$2	$4" >> $W/raw/query_log.tsv
$PY $SKILL_DIR/scripts/aii_fast_web_fetch.py grep --url "$2" --pattern "$4" -i --max-matches ${5:-15} --context-chars 300 > $W/raw/fetch/$1.txt 2>&1
else
echo "$(date -u +%FT%TZ)	fetch	$1	$2" >> $W/raw/query_log.tsv
$PY $SKILL_DIR/scripts/aii_fast_web_fetch.py fetch --url "$2" --max-chars ${3:-12000} > $W/raw/fetch/$1.txt 2>&1
fi
