#!/bin/bash
awk '{system("python main_file.py "$1)}' $1
