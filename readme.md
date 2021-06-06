Code Comparator
===============

Prerequisites
-------------
* Python, at least version 3.8.
* Java, at least version 8.

Running
-------
1. Make `Code Comparator` the current directory.

2. Create a virtual environment in the project directory: `python3 -m venv venv` (Windows: `py -3 -m venv venv`)

3. Activate the virtual environment: `. venv/bin/activate` (Windows: `venv\Scripts\activate`)

4. Install Flask: `pip install Flask`

5. Install Markdown: `pip install markdown`

6. Set environment variables: `export FLASK_APP=code_comparator`, `export FLASK_ENV=development` (Windows: `set FLASK_APP=code_comparator`, `set FLASK_ENV=development`)

7. Initialize the database: `flask initialize-database`

8. Start Flask: `flask run`

9. Go to `http://127.0.0.1:5000` in your web browser.