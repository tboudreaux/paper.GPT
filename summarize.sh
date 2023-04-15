#!/bin/bash
#
datetime=$(date)
DOW=$(date +%u)
root="/home/tboudreaux/d/Documents/Emily/Programming/paper.GPT"
home="/home/tboudreaux"
pythonEXE=/home/tboudreaux/anaconda3/envs/GPT/bin/python
echo "[$datetime : info] starting" >> "$root/summary.log"
if [ $DOW != 6 ] && [$DOW != 7]; then
	echo "[$datetime : info] It's a weekday, let's summarize the new papers." >> "$root/summary.log"
	echo "[$datetime : info] Querying arXiv for new papers." >> "$root/summary.log"
	$pythonEXE "$root/queryArxiv.py"
	echo "[$datetime : info] Summarizing new papers." >> "$root/summary.log"
	$pythonEXE "$root/arxivSummary.py"
	echo "[$datetime : info] Copying summary to website." >> "$root/summary.log"
	cp "$root/summaryResults.html" "$home/public_html/files"
	echo "[$datetime : info] Sending summary email." >> "$root/summary.log"
	$pythonEXE "$root/sendSummary.py"
else
	echo "[$datetime : info] It's the weekend, no new papers to summarize." >> "$root/summary.log
fi

echo "[$datetime : info] complete" >> "$root/summary.log"

