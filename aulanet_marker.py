"""A script that inputs marks on AulaNet from an Excel file source."""

import csv
import re

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys


class AulaNetSession:
    """The browser session and functions."""

    def __init__(self):
        """Open session by opening the web browser, identifying as Chrome."""
        options = Options()
        options.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        )
        self.browser = webdriver.Firefox(options=options)
        self.browser.get("https://erp.aulanet.com.mx")

    def get_students(self):
        """Get students from webpage."""
        self.students = (
            self.browser.find_elements("class name", "CS_even")
            + self.browser.find_elements("class name", "CS_odd")
        )

    def get_info(self, student):
        """Get student’s ID number and name."""
        regex = re.compile(r"^(\d{6})\n(.+?)\n")
        return list(map(str.title, regex.search(student.text).groups()))

    def input_marks(self, student, marks):
        """
        Input marks in each box.

        Inputs:
            student, a Selenium object.
            marks, a list of ints.
        """
        boxes = student.find_elements("class name", "CS_calificacion")
        marks_data = dict(zip(boxes, marks))
        for box, mark in marks_data.items():
            for x in range(10):
                box.send_keys(Keys.BACK_SPACE)
            box.send_keys(mark)

    def input_marks_all(self, marks_data):
        """
        Input marks for all students on the page.

        Inputs: marks_data, a dictionary.
        """
        for student in self.students:
            self.input_marks(
                student, marks_data.get(self.get_info(student)[0])
            )

    def write_csv(self, filename):
        """
        Write students’ information to CSV file.

        Inputs: filename, a csv file.
        """
        file = open(filename, "a")
        writer = csv.writer(file)
        for item in self.students:
            writer.writerow(self.get_info(item) + ["", "", "", "", ""])
        file.close()

    def close_browser(self):
        """Close sessions."""
        self.browser.close()


def get_marks(marks_file):
    """
    Parse students’ information from CSV.

    Returns:a dictionary.
    """
    file = open(marks_file)
    reader = csv.reader(file)
    student_data = list(reader)
    final = {}
    for student in student_data:
        final.setdefault(
            student[0], [int(student[x]) for x in range(2, len(student))]
        )
    return final


def aulanet_marker():
    """Open session and awaits input to parse and copy marks."""
    print("Opening web browser …")
    session = AulaNetSession()
    print("Please manually log into AulaNet.")
    while True:
        choice = input(
            "Press q to quit, s to save page data to marks.csv, "
            "and any other key to input marks on this page. "
        )
        if choice == "q":
            session.close_browser()
            break
        elif choice == "s":
            session.get_students()
            session.write_csv("marks.csv")
        else:
            session.get_students()
            session.input_marks_all(get_marks("marks.csv"))
        print("Done with this page.")


aulanet_marker()
