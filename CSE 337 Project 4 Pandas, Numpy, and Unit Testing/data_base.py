"""Calculate student grades by combining data from many sources.

Using Pandas, this script combines data from the:

* Roster
* Homework & Exam grades
* Quiz grades

to calculate final grades for a class.
"""
#Importing Libraries and Setting Paths
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

HERE = Path(__file__).parent
DATA_FOLDER = HERE / "data"

#Data Importation and Cleaning
roster = pd.read_csv(
    filepath_or_buffer = DATA_FOLDER / "roster.csv",
    index_col = "NetID",
    usecols = ["Section", "Email Address", "NetID"],
    converters = {"NetID": str.lower, "Email Address": str.lower},
)

hw_exam_grades = pd.read_csv(
    filepath_or_buffer = DATA_FOLDER / "hw_exam_grades.csv",
    index_col = "SID",
    usecols = [theColumn for theColumn in pd.read_csv(DATA_FOLDER / "hw_exam_grades.csv").columns if "Submission" not in theColumn],
    converters = {"SID": str.lower},
)

quiz_grades = pd.DataFrame()
#Your code here to read the quiz_grades

for data_file_directory in DATA_FOLDER.glob("quiz_*_grades.csv"):
    file_parts = data_file_directory.stem.split("_")
    quiz_title = " ".join(data_file_directory.stem.title().split("_")[:2])

    quiz_grades_data = pd.read_csv(
        filepath_or_buffer = data_file_directory,
        index_col = ["Email"],
        usecols = ["Email", "Grade"],
        converters = {"Email": str.lower},
    )
    quiz_grades_data = quiz_grades_data.rename(columns={"Grade": quiz_title})

    if data_file_directory:
        file_parts = file_parts
        quiz_grades = pd.concat([quiz_grades, quiz_grades_data], axis = 1)

#Data Merging: roster and homework
final_data = pd.merge(roster, hw_exam_grades, right_index = True, left_index = True)

#Data Merging: Final data and quiz grades
final_data = pd.merge(final_data, quiz_grades, right_index = True, left_on = "Email Address")

final_data = final_data.fillna(0)

#Data Processing and Score Calculation
n_exams = 3
#For each exam, calculate the score as a proportion of the maximum points possible.
#Remove pass once you have cerated written the for loop
for n in range(1, n_exams + 1):
    final_data[f"Exam {n} Score"] = final_data[f"Exam {n}"] / final_data[f"Exam {n} - Max Points"]

#Calculating Exam Scores:
#Filter homework and Homework - for max points
homework_scores = final_data.filter(axis = 1, regex = r"^Homework \d\d?$")
homework_max_points = final_data.filter(axis = 1, regex = r"^Homework \d\d? -")

#Calculating Total Homework score
sum_of_hw_scores = homework_scores.sum(axis = 1)
sum_of_hw_max = homework_max_points.sum(axis = 1)
final_data["Total Homework"] = sum_of_hw_scores / sum_of_hw_max

#Calculating Average Homework Scores
hw_max_renamed = homework_max_points.set_axis(axis = 1, labels = homework_scores.columns)
average_hw_scores = (homework_scores / hw_max_renamed).sum(axis = 1)
final_data["Average Homework"] = average_hw_scores / homework_scores.shape[1]

#Final Homework Score Calculation
final_data["Homework Score"] = final_data[["Total Homework", "Average Homework"]].max(axis = 1)

#Calculating Total and Average Quiz Scores:
#Filter the data for Quiz scores
quiz_scores = final_data.filter(axis = 1, regex = r"^Quiz \d$")

quiz_max_points = pd.Series(
    {"Quiz 1": 11, "Quiz 2": 15, "Quiz 3": 17, "Quiz 4": 14, "Quiz 5": 12}
)

#Final Quiz Score Calculation:
sum_of_quiz_scores = quiz_scores.sum(axis = 1)
sum_of_quiz_max = quiz_max_points.sum()
final_data["Total Quizzes"] = sum_of_quiz_scores / sum_of_quiz_max

average_quiz_scores = (quiz_scores / quiz_max_points).sum(axis = 1)
final_data["Average Quizzes"] = average_quiz_scores / quiz_scores.shape[1]

final_data["Quiz Score"] = final_data[["Total Quizzes", "Average Quizzes"]].max(axis = 1)

#Calculating the Final Score:
weightings = pd.Series(
    {
        "Exam 1 Score": 0.05,
        "Exam 2 Score": 0.1,
        "Exam 3 Score": 0.15,
        "Quiz Score": 0.30,
        "Homework Score": 0.4,
    }
)

final_data["Final Score"] = (final_data[weightings.index] * weightings).sum(axis = 1)

#Rounding Up the Final Score
final_data["Ceiling Score"] = np.ceil(final_data["Final Score"] * 100)

#Defining Grade Mapping:
grades = {
    90: "A",
    80: "B",
    70: "C",
    60: "D",
    0: "F",
}

#Applying Grade Mapping to Data:
def grade_mapping(value):
    for grade_value_key, letter_grade_value in grades.items():
        if value >= grade_value_key:
            return letter_grade_value
        else:
            continue

letter_grades = final_data["Ceiling Score"].map(grade_mapping)
final_data["Final Grade"] = pd.Categorical(values = letter_grades, ordered = True, categories = grades.values())

#Processing Data by Sections:
for section, table in final_data.groupby("Section"):
    data_file_in_section = DATA_FOLDER / f"Section {section} Grades.csv"
    sorted_table = table.sort_values(by = ["Last Name", "First Name"])
    print(f"In Section {section} there are {table.shape[0]} students saved to "f"file {data_file_in_section}.")
    sorted_table.to_csv(data_file_in_section)

#Visualizing Grade Distribution: Get Grade Counts and use plot to plot the grades
grade_counts = final_data["Final Grade"].value_counts().sort_index()

grade_counts.plot.bar()
plt.show()

#Visualize the data on with Histogram and use Matplot lib density function to print Kernel Density Estimate
final_data["Final Score"].plot.hist(bins=20, label="Histogram")
final_data["Final Score"].plot.density(
    linewidth=4, label="Kernel Density Estimate"
)

#Plotting Normal Distribution:
final_mean = final_data["Final Score"].mean()
final_std = final_data["Final Score"].std()

#Plot the normal distribution of final_mean and final_std
stats_normal_distribution = scipy.stats.norm.pdf(np.linspace(final_mean - 5 * final_std, final_mean + 5 * final_std, 200), scale = final_std, loc = final_mean)
plt.plot(np.linspace(final_mean - 5 * final_std, final_mean + 5 * final_std, 200), stats_normal_distribution, label = "Normal Distribution", linewidth = 4)
plt.legend()
plt.show()
