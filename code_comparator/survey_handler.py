import uuid
import datetime
from flask import (Blueprint, render_template, request, session, redirect,
  url_for)
from code_comparator.database import get_database

# Creates a survey handler blueprint.
blueprint = Blueprint("survey_handler", __name__)

@blueprint.route("/", methods=("GET", "POST"))
def index():
  """The survey view."""

  # Executes if the view is called with a POST request.
  if request.method == 'POST':

    # Stores the survey answers.
    
    age_group = request.form["age_group"]

    gender = request.form["gender"]
    
    occupation = request.form["occupation"]

    other_occupation_description = request.form[
      "other_occupation_description"]
    
    occupation_time = request.form["occupation_time"]

    software_development_frequency = request.form[
      "software_development_frequency"]

    programming_experience = request.form["programming_experience"]


    java_course = "yes" if request.form.get("java_course", None) else "no"

    rxjava_course = "yes" if request.form.get("rxjava_course", None) else "no"


    basic = "yes" if request.form.get("basic", None) else "no"

    prolog = "yes" if request.form.get("prolog", None) else "no"

    haskell = "yes" if request.form.get("haskell", None) else "no"

    java = "yes" if request.form.get("java", None) else "no"

    sql = "yes" if request.form.get("sql", None) else "no"

    c = "yes" if request.form.get("c", None) else "no"

    cpp = "yes" if request.form.get("cpp", None) else "no"

    cs = "yes" if request.form.get("cs", None) else "no"

    python = "yes" if request.form.get("python", None) else "no"

    javascript = "yes" if request.form.get("javascript", None) else "no"

    assembly = "yes" if request.form.get("assembly", None) else "no"


    java_knowledge = request.form["java_knowledge"]

    reactive_programming_experience = request.form[
      "reactive_programming_experience"]

    rxjava_knowledge = request.form["rxjava_knowledge"]

    # Generates a unique test subject id.
    test_subject_id = str(uuid.uuid4())

    # Clears session.
    session.clear()

    # Stores the test subject id in session.
    session["test_subject_id"] = test_subject_id

    # Stores the introduction started timestamp.
    introduction_started = str(datetime.datetime.now())

    # Retrieves the database.
    database = get_database()

    # Creates a database command to update the test subject relation with the
    # survey answers.
    database.execute("INSERT INTO test_subject ("
      "id, "
      "age_group, "
      "gender, "
      "occupation, "
      "other_occupation_description, "
      "occupation_time, "
      "software_development_frequency, "
      "programming_experience, "
      "java_course, "
      "rxjava_course, "
      "basic, "
      "prolog, "
      "haskell, "
      "java, "
      "sql, "
      "c, "
      "cpp, "
      "cs, "
      "python, "
      "javascript, "
      "assembly, "
      "java_knowledge, "
      "reactive_programming_experience, "
      "rxjava_knowledge, "
      "introduction_started) "
      "VALUES "
      "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
      "?, ?, ?);",
      (test_subject_id, age_group, gender, occupation,
      other_occupation_description, occupation_time,
      software_development_frequency, programming_experience, java_course,
      rxjava_course, basic, prolog, haskell, java, sql, c, cpp, cs, python,
      javascript, assembly, java_knowledge, reactive_programming_experience,
      rxjava_knowledge, introduction_started))

    # Executes the database command.
    database.commit()

    # Stores a redirect to the introduction web page in the return value.
    return_value = redirect(url_for("code_snippet_handler.introduction"))

  else:

    # Stores the survey web page in the return value.
    return_value = render_template("survey_handler/survey.html")


  # Returns the resulting web page to the caller.
  return return_value