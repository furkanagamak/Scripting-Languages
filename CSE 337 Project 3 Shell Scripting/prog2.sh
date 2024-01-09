#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "data file or output file not found"
    exit 1
fi

given_data_file="$1"
given_output_file="$2"

if [ ! -f "$given_data_file" ]; then
    echo "$given_data_file not found"
    exit 1
fi

awk -F '[,;:]' '
{
    for (file_index = 1; file_index <= NF; file_index++) {
        sum[file_index] += $file_index
    }
    if (NF > maximum_columns) {
        maximum_columns = NF
    }
}
END {
    for (file_index = 1; file_index <= maximum_columns; file_index++) {
        print "Col " file_index " : " sum[file_index]
    }
}' "$given_data_file" > "$given_output_file"
