#!/usr/bin/env bash
cd "$(dirname "$0")/.."
PID=$(cat logs/passA.pid)
while kill -0 $PID 2>/dev/null; do sleep 15; done
n=$(ls passA/parts/done_*.json | wc -l)
if [ "$n" -lt 2040 ]; then .venv/bin/python passA.py --workers 5 >> logs/passA_stdout.log 2>&1; fi
echo "passA done files: $(ls passA/parts/done_*.json | wc -l)"
.venv/bin/python passA.py --merge > logs/passA_merge.log 2>&1 && echo "merge ok"
nohup .venv/bin/python passB.py --workers 5 > logs/passB_stdout.log 2>&1 &
echo $! > logs/passB.pid
.venv/bin/python tests/checks.py A > logs/checksA.log 2>&1; echo "checks A exit $?"
.venv/bin/python build_features.py --stage basic > logs/features_basic.log 2>&1; echo "basic exit $?"
rm -rf data/ego_timing
.venv/bin/python build_features.py --timing 60 --workers 5 > logs/t4.log 2>&1; echo "t4 exit $?"
echo CHAIN1_DONE
