Code Comparator
===============

About
-----
This tool measures the time needed to correct errors in Java code snippets, as a way of determining code comprehensibility. The code snippets are implemented according to one of two paradigms; procedural or reactive.
Code Comparator is divided into three parts:
1. Survey
2. Introduction
3. Comprehensibility test.


When started, the user is presented with a survey form, followed by an eight part introduction to Java and RxJava. The comprehensibility test can be started from the introduction at the user's discretion.

Prerequisites
-------------
* Python, at least version 3.8.
* Java, at least version 8.

Running
-------
1. Make the directory containing this readme file the current directory.

2. Create a virtual environment in the project directory: `python3 -m venv venv` (Windows: `py -3 -m venv venv`)

3. Activate the virtual environment: `. venv/bin/activate` (Windows: `venv\Scripts\activate`)

4. Install Flask: `pip3 install Flask`

5. Install Markdown: `pip3 install markdown`

6. Set environment variables: `export FLASK_APP=code_comparator`, `export FLASK_ENV=development` (Windows: `set FLASK_APP=code_comparator`, `set FLASK_ENV=development`)

7. Initialize the database: `flask initialize-database`

8. Start Flask: `flask run`

9. Go to `http://127.0.0.1:5000` in your web browser.

10. The collected data, i.e. survey answers and comprehensibility test results are persisted to a SQLite database: `code_comparator/instance/code_comparator.sqlite`.

Customizing
-----------
The survey content is in `code_comparator/templates/survey_handler/survey.html` and the logic for the survey is in `code_comparator/survey_handler.py`.

Each introduction part consists of information in a markdown file and code examples in a text file. The introduction files are in `code_comparator/introduction`. Please update `NUMBER_OF_INTRODUCTION_PARTS` in `code_comparator/code_snippet_handler.py` if introduction parts are added or removed.

The code snippets for the comprehensibility test and associated instructions are located in the `comprehensibility_test` folder, sorted into subfolders per paradigm. Code snippets should be added in pairs, one procedural and one reactive variant per functionality to be tested. Please update `TOTAL_NUMBER_OF_COMPREHENSIBILITY_TESTS` and `NUMBER_OF_COMPREHENSIBILITY_TESTS_PER_TEST_SUBJECT` in `code_comparator/code_snippet_handler.py` with the total number of comprehensibility test pairs and the number of tests per test subject respectively.

When changing the survey or the number of comprehensibility tests the database schema, `code_comparator/schema.sql`, must be updated together with affected database calls.

External projects
-----------------
This project uses the following external OSS projects:

* **Flask**, a lightweight WSGI web application framework.
https://github.com/pallets/flask

* **RxJava**, reactive Extensions for the JVM.
https://github.com/ReactiveX/RxJava/tree/2.x

* **Ace**, a standalone code editor written in JavaScript.
https://github.com/ajaxorg/ace


