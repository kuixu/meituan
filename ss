#!/bin/bash
awk 'BEGIN{p=0}NR==1{t=$4}$1==1{p++}NR>1{s+=$2}END{print "TotalComm: "t,"CurrentComm: "NR,"Pic: "p,"PicRate: "p/NR,"Avg.Score: "s/(NR*100)}' $1
