#!/bin/bash
ls futian/*.txt|awk '{system("./ss "$1)}'
