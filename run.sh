#!/bin/bash
nohup python -u regular_report.py > regular_report.log &
nohup python -u offline_report.py > offline_report.log &
