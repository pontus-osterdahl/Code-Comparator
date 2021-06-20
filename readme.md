Code Comparator
===============

About
-----
This tool measures the time needed to correct errors in Java code snippets, as a way of determining code comprehensibility. The code snippets are implemented according to one of two paradigms; procedural or reactive. When started, the user is presented with a survey form, followed by an eight part introduction to Java and RxJava. The comprehensibility test can be started from the introduction at the user's discretion.

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

Customizing
-----------
The survey content is in code_comparator/templates/survey_handler/survey.html and the logic is in code_comparator/survey_handler.py. Each introduction part consists of information in a markdown file and code examples in a text file. The introduction files are in code_comparator/introduction.

External projects
-----------------
This project uses the following external OSS projects:

* **Flask**, a lightweight WSGI web application framework.
https://github.com/pallets/flask

* **RxJava**, reactive Extensions for the JVM.
https://github.com/ReactiveX/RxJava/tree/2.x

* **Ace**, a standalone code editor written in JavaScript.
https://github.com/ajaxorg/ace


