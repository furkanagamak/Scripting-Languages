#!/usr/bin/env ruby

arguments_arr = ARGV

# check for minimum number of arguments
if arguments_arr.length < 1
  puts "Missing required arguments"
  exit
end

source_filename = arguments_arr[0]

# check if file exists
unless File.exist?(source_filename)
  puts "File not found"
  exit
end

source_file_content = File.read(source_filename).split("\n")

# extract options and patterns
all_options_arr = arguments_arr[1..-1].select { |arg| arg.start_with?("-") }
all_patterns_arr = arguments_arr[1..-1].reject { |arg| arg.start_with?("-") }

# check for invalid options
all_options_arr.each do |theOptions|
  unless ["-w", "-p", "-v", "-c", "-m"].include?(theOptions)
    puts "Invalid option"
    exit
  end
end

# error if no patterns
if all_patterns_arr.empty?
  puts "Missing required arguments"
  exit
end

# error if more than 1 pattern
if all_patterns_arr.size != 1
  puts "Invalid option"
  exit
end

# default option is -p if valid filename and pattern are provided
if all_options_arr.empty? && all_patterns_arr.size == 1
  all_options_arr << "-p"
end

# check for invalid combinations of options
if all_options_arr.include?("-v") && all_options_arr.include?("-m")
  puts "Invalid combination of options"
  exit
end

# helper method to validate options
def valid_option_combinations(all_options_arr)
  single_options = ["-w", "-p", "-v"]
  double_options = ["-c", "-m"]

  # invalid option if no main options are present
  main_options_present = (all_options_arr - double_options)
  
  if main_options_present.empty?
    puts "Invalid option"
    exit
  end

  # there should be exactly one of the single_options and zero or one of the double_options
  main_options_present.size == 1 && (all_options_arr - single_options).size <= 1
end

# check for valid combinations
unless valid_option_combinations(all_options_arr)
  puts "Invalid combination of options"
  exit
end

# perform required options
if all_options_arr.include?("-w")
  pattern_downcase = all_patterns_arr[0].downcase
  matching_lines_from_file = source_file_content.select do |line| 
    line.downcase.split.any? { |word| word.start_with?(pattern_downcase) }
  end
elsif all_options_arr.include?("-p")
  regex_file_search = Regexp.new(all_patterns_arr[0])
  matching_lines_from_file = source_file_content.select { |line| regex_file_search.match?(line) }
elsif all_options_arr.include?("-v")
  regex_file_search = Regexp.new(all_patterns_arr[0])
  matching_lines_from_file = source_file_content.reject { |line| regex_file_search.match(line) }
end

# perform -m and -c options
if all_options_arr.include?("-m")
  if all_options_arr.include?("-w")
    regex_file_search = Regexp.new("\\b#{all_patterns_arr[0]}", Regexp::IGNORECASE)
    puts matching_lines_from_file.map { |line| line.scan(regex_file_search).join(" ") }.join("\n")
  elsif all_options_arr.include?("-p")
    regex_file_search = Regexp.new(all_patterns_arr[0])
    puts matching_lines_from_file.map { |line| line.scan(regex_file_search).join(" ") }.join("\n")
  end

elsif all_options_arr.include?("-c")
  puts matching_lines_from_file.size
else
  puts matching_lines_from_file.join("\n")
end