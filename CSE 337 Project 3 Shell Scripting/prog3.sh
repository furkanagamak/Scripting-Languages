#!/bin/bash

if [ -z "$1" ]; then
    echo "missing data file"
    exit 1
fi

given_student_scores_file="$1"

if [ ! -f "$given_student_scores_file" ]; then
    echo "Error: File '$given_student_scores_file' not found."
    exit 1
fi

shift

given_student_scores_weights=("$@")

awk -F, -v given_exam_weights="${given_student_scores_weights[*]}" '
BEGIN {
    split(given_exam_weights, assigned_weights, " ")
    num_exam_weights = length(assigned_weights)
    total_exam_weights = 0
    total_student_scores = 0
    total_student_count = 0
}

{
    individual_student_exam_score = 0
    individual_student_exam_weight = 0
    for (loop_index = 2; loop_index <= NF; loop_index++) {
        current_student_weight_index = loop_index - 1
        current_student_weight = (current_student_weight_index <= num_exam_weights) ? assigned_weights[current_student_weight_index] : 1
        individual_student_exam_score += $loop_index * current_student_weight
        individual_student_exam_weight += current_student_weight
    }
    total_student_scores += individual_student_exam_score
    total_exam_weights += individual_student_exam_weight
    total_student_count++
}

END {
    if (total_student_count == 0 || total_exam_weights == 0) {
        print "Error: No students found or total weight is zero."
        exit 1
    }
    weightedAverage = int(total_student_scores / total_exam_weights)
    print weightedAverage
}' "$given_student_scores_file"
