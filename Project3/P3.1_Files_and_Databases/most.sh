#!/bin/bash

awk '
BEGIN {FS = ","};
{array[$7]+=$3;array2[$7]=$9}
END {for(i in array) {print array[i]","i","array2[i]}}
' million_songs_metadata_and_sales.csv | sort -n | tail -2
