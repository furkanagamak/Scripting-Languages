#!/bin/bash

helper_function_for_moving_c_files() {
    echo "Moving files from $1 to $2:"
    for c_file_to_be_moved in "$1"/*.c; do
        [ -e "$c_file_to_be_moved" ] || continue
        echo "Moving $c_file_to_be_moved"
        read -p "Confirm moving file (y/n): " userConfirmMove
        if [[ $userConfirmMove == [yY] ]]; then
            mv "$c_file_to_be_moved" "$2"
        fi
    done
}

if [ "$#" -ne 2 ]; then
    echo "src and dest dirs missing"
    exit 1
fi

given_source_directory=$1
given_destination_directory=$2

if [ ! -d "$given_source_directory" ]; then
    echo "$given_source_directory not found"
    exit 0
fi

for theDirectory in $(find "$given_source_directory" -type d); do
    created_new_directory=${theDirectory/$given_source_directory/$given_destination_directory}
    
    if [ ! -d "$created_new_directory" ]; then
        mkdir -p "$created_new_directory" || { echo "Failed to create directory $created_new_directory"; exit 1; }
    fi

    number_of_c_files=$(ls "$theDirectory"/*.c 2>/dev/null | wc -l)
    if [ "$number_of_c_files" -gt 3 ]; then
        helper_function_for_moving_c_files "$theDirectory" "$created_new_directory"
    elif [ "$number_of_c_files" -gt 0 ]; then
        mv "$theDirectory"/*.c "$created_new_directory"
    fi
done
