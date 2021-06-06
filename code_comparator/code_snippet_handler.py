from flask import (Blueprint, render_template, request, Markup, session,
  redirect, url_for)
import shutil
from pathlib import Path
import markdown
import subprocess
import os
import platform
import datetime
import random
from flask.json import jsonify
from code_comparator.database import get_database


# The introduction folder.
INTRODUCTION_FOLDER = r"code_comparator/introduction/"

# The number of introduction parts.
NUMBER_OF_INTRODUCTION_PARTS = 8

# The folder with procedural comprehensibility tests.
PROCEDURAL_COMPREHENSIBILITY_TEST_FOLDER = (
  r"code_comparator/comprehensibility_test/procedural/")

# The folder with reactive comprehensibility tests.
REACTIVE_COMPREHENSIBILITY_TEST_FOLDER = (
  r"code_comparator/comprehensibility_test/reactive/")

# The total number of comprehensibility tests.
TOTAL_NUMBER_OF_COMPREHENSIBILITY_TESTS = 4

# The number of comprehensibility tests per subject.
NUMBER_OF_COMPREHENSIBILITY_TESTS_PER_TEST_SUBJECT = 4

# The Java code snippet suffix.
CODE_SNIPPET_SUFFIX = ".txt"

# The information file suffix.
INFORMATION_FILE_SUFFIX = ".md"

# The path to the first part of the Java Main class.
JAVA_MAIN_BEGINNING = r"code_comparator/building_blocks/java_main_beginning.txt"

# The path to the last part of the Java Main class.
JAVA_MAIN_END = r"code_comparator/building_blocks/java_main_end.txt"

# The path to the joined Java Main class.
RESULT_FILENAME = r"temporary/Main.java"

# The macOS system name.
MACOS_SYSTEM_NAME = "Darwin"

# The Linux system name.
LINUX_SYSTEM_NAME = "Linux"

# The Windows system name.
WINDOWS_SYSTEM_NAME = "Windows"

# Unknown operation system message.
UNKNOWN_SYSTEM_MESSAGE = "Unknown operating system!"

# The macOS command for compiling the Java Main class.
MACOS_COMPILATION_COMMAND = "javac -cp 'JARs/*' "

# The Linux command for compiling the Java Main class.
LINUX_COMPILATION_COMMAND = "javac -cp 'JARs/*' "

# The Windows command for compiling the Java Main class.
WINDOWS_COMPILATION_COMMAND = "javac -cp JARs/* "

# The macOS command for executing the Java Main class.
MACOS_EXECUTION_COMMAND = "java -cp .:../JARs/* Main"

# The Linux command for executing the Java Main class.
LINUX_EXECUTION_COMMAND = "java -cp .:../JARs/* Main"

# The Windows command for executing the Java Main class.
WINDOWS_EXECUTION_COMMAND = "java -cp .;../JARs/* Main"

# An integer to word translator.
INTEGER_TO_WORD = {
  1: "one",
  2: "two",
  3: "three",
  4: "four"
}


# Creates a code snippet handler blueprint.
blueprint = Blueprint("code_snippet_handler", __name__,
  url_prefix="/code_snippet_handler")


@blueprint.route("/introduction", methods = ('GET', 'POST'))
def introduction():
  """The introduction view."""
  
  # Executes if the view is called with a GET request.
  if request.method == 'GET':
    
    # Executes if the user clicked the previous button.
    if request.args.get("previous_part", None):

      # Executes if the current introduction part is not the first
      # introduction part.
      if session["current_introduction_part"] != 1:

        # Moves to the previous introduction part.
        session["current_introduction_part"] -= 1

    # Executes if the user clicked the next button.
    elif request.args.get("next_part", None):

      # Executes if the current introduction part is not the last
      # introduction part.
      if session["current_introduction_part"] != NUMBER_OF_INTRODUCTION_PARTS:

        # Moves to the next introduction part.
        session["current_introduction_part"] += 1

    # Executes if this is the first view execution.
    else:

      # Initializes the current introduction part to the first introduction
      # part.
      session["current_introduction_part"] = 1

      # Retrieves the time when the introduction started.
      introduction_started = datetime.datetime.now().isoformat()

      # Retrieves the database.
      database = get_database()

      # Persists the introduction started time to the database.
      database.execute("UPDATE test_subject "
        "SET introduction_started = ? "
        "WHERE id = ?;",
        (introduction_started, session["test_subject_id"]))

      # Commits the database transaction.
      database.commit()


    # Constructs the path to the current introduction information file.
    introduction_information_path = Path(INTRODUCTION_FOLDER +
      str(session["current_introduction_part"]) + INFORMATION_FILE_SUFFIX)

    # Constructs the path to the current introduction code snippet file.
    introduction_code_snippet_path = Path(INTRODUCTION_FOLDER +
      str(session["current_introduction_part"]) + CODE_SNIPPET_SUFFIX)

    # Initializes the information.
    information = ""
    
    # Opens the introduction information file.
    with open(introduction_information_path, "r") as information_file:

      # Creates an introduction part header.
      header = ("Introduction part " +
        str(session["current_introduction_part"]) + " of " +
        str(NUMBER_OF_INTRODUCTION_PARTS) + " - ")

      # Stores the information.
      information = Markup(markdown.markdown(header + information_file.read()))

    # Initializes the code snippet.
    code_snippet = ""
    
    # Opens the introduction code snippet file.
    with open(introduction_code_snippet_path, "r") as code_snippet_file:

      # Stores the code snippet.
      code_snippet = code_snippet_file.read()


    # Stores a web page with the introduction code snippet and information in
    # the return value.
    return_value = render_template('code_snippet_handler/introduction.html',
      code_snippet = code_snippet, information = information)

  # Executes if the view is called with a POST request.
  else:

    # Executes if the user clicked the start comprehensibility test button.
    if request.form.get("start_comprehensibility_test", None):

      # Stores a redirect to the comprehensibility test web page in the return
      # value.
      return_value = redirect(url_for(
        "code_snippet_handler.comprehensibility_test"))

    # Executes if the user clicked the execute button.
    else:

      # Stores the result of compiling and executing the code snippet in the
      # return value.
      return_value = compile_and_execute(request.form['code_snippet_area'])

  # Returns the resulting web page to the caller.
  return return_value


@blueprint.route("/comprehensibility_test", methods = ('GET', 'POST'))
def comprehensibility_test():
  """The comprehensibility test view."""

  # Executes if the view is called with a GET request.
  if request.method == 'GET':

    # Initializes the test.
    initialize_comprehensibility_test()

    # Prepares the first test page.
    return_value = create_next_comprehensibility_test(False)


  # Executes if the view is called with a POST request.
  else:

    # Retrieves the code snippet from the web page.
    code_snippet = request.form['code_snippet_area']
    
    # Executes if the user clicked the finish button.
    if request.form.get("finish", None):

      # Finishes the current comprehensibility test.
      finish_current_comprehensibility_test(code_snippet)

      # Executes if the last comprehensibility test was finished.
      if session["current_test"] == (
        NUMBER_OF_COMPREHENSIBILITY_TESTS_PER_TEST_SUBJECT):

        # Updates the web page with a test finished message.
        return_value = jsonify(finito = True, code_snippet = "", information =
          "The comprehensibility test is finished. "
          "Thank you for your cooperation!")

      # Executes if the finished comprehensibility test was not the last.
      else:

        # Stores a new comprehensibility test in the return value.
        return_value = create_next_comprehensibility_test(True)

    # Executes if the user clicked the execute button.
    else:

      # Stores the result of compiling and executing the code snippet in the
      # return value.
      return_value = compile_and_execute(code_snippet)


  # Returns the resulting web page to the caller.
  return return_value


def initialize_comprehensibility_test():
  """Initializes the comprehensibility test."""

  # Picks random test numbers.
  test_numbers = random.sample(range(1,
    TOTAL_NUMBER_OF_COMPREHENSIBILITY_TESTS + 1),
    NUMBER_OF_COMPREHENSIBILITY_TESTS_PER_TEST_SUBJECT)

  # Stores test code snippets.
  code_snippets = []

  # Stores test instructions.
  instructions = []

  # Determines if the first test is procedural or reactive.
  start_number = random.randint(0, 1)

  # Iterates over the test numbers.
  for index, test_number in enumerate(test_numbers, start=start_number):

    # Selects a procedural test if the index is even, selects a reactive test
    # otherwise.
    folder = (PROCEDURAL_COMPREHENSIBILITY_TEST_FOLDER if index % 2 == 0 else
      REACTIVE_COMPREHENSIBILITY_TEST_FOLDER)

    # Stores the path to the code snippet.
    code_snippets.append(str(Path(folder, str(test_number) +
      CODE_SNIPPET_SUFFIX)))

    # Stores the path to the instruction.
    instructions.append(str(Path(folder, str(test_number) +
      INFORMATION_FILE_SUFFIX)))

  # Stores the code snippets in session.
  session["code_snippets"] = code_snippets

  # Stores the instructions in session.
  session["instructions"] = instructions

  # Resets current test.
  session["current_test"] = 0


def create_next_comprehensibility_test(is_response):
  """Creates a comprehensibility test."""
  
  # Initializes the instruction container.
  instruction = ""

  # Opens the instruction file.
  with open(Path(session["instructions"][session["current_test"]]),
    "r") as instruction_file:

    # Creates test header.
    header = ("### Test " + str(session["current_test"] + 1) + " of " +
      str(NUMBER_OF_COMPREHENSIBILITY_TESTS_PER_TEST_SUBJECT) + " ")
    
    # Stores the instruction.
    instruction = Markup(markdown.markdown(header + instruction_file.read()))

  # Initializes the code snippet container.
  code_snippet = ""

  # Opens the code snippet file.
  with open(Path(session["code_snippets"][session["current_test"]]),
    "r") as code_snippet_file:

    # Stores the code snippet.
    code_snippet = code_snippet_file.read()

  # Stores the test started timestamp.
  test_started = datetime.datetime.now().isoformat()

  # Stores the test started timestamp in session.
  session["test_started"] = test_started

  # Creates a string for the current test.
  test_string = "test_" + INTEGER_TO_WORD[session["current_test"] + 1]

  # Creates a test started string.
  test_started_string = test_string + "_started"

  # Retrieves the database.
  database = get_database()

  # Updates the test_subject with the current code snippet path and the test
  # started timestamp.
  database.execute("UPDATE test_subject "
    "SET " + test_string + " = ?, " +
    test_started_string + " = ? "
    "WHERE id = ?;",
    (session["code_snippets"][session["current_test"]],
    test_started, session["test_subject_id"]))

  # Commits the database command.
  database.commit()

  # Executes if the function should generate an answer to an XMLHttpRequest.
  if is_response:
    
    # Updates the web page with the new code snippet and instruction.
    return_value = jsonify(code_snippet = code_snippet,
      information = instruction)

  # Executes if this is the initial function call.
  else:

    # Creates a web page with the new code snippet and instruction.
    return_value = render_template(
      'code_snippet_handler/comprehensibility_test.html',
      code_snippet = code_snippet, information = instruction)

  # Returns an updated comprehensibility test web page.
  return return_value


def finish_current_comprehensibility_test(code_snippet):
  """Finishes the current comprehensibility test."""

  # Stores the test ended timestamp.
  test_ended = datetime.datetime.now().isoformat()

  # Stores the test duration in seconds.
  test_duration = str((datetime.datetime.fromisoformat(test_ended) -
    datetime.datetime.fromisoformat(session["test_started"])).total_seconds())

  # Stores the test result.
  test_result = code_snippet

  # Creates a test string.
  test_string = "test_" + INTEGER_TO_WORD[session["current_test"] + 1]

  # Creates a test ended string.
  test_ended_string = test_string + "_ended"

  # Creates a test duration string.
  test_duration_string = test_string + "_duration_in_seconds"

  # Creates a test result string.
  test_result_string = test_string + "_result"

  # Retrieves the database.
  database = get_database()

  # Creates a database command to update the test subject relation with test
  # ended timestamp, test duration and test result.
  database.execute("UPDATE test_subject "
    "SET " + test_ended_string + " = ?, " +
    test_duration_string + " = ?, " +
    test_result_string + " = ? "
    "WHERE id = ?;",
    (test_ended, test_duration, test_result, session["test_subject_id"]))

  # Executes the database command.
  database.commit()
  
  # Sets current test to the next test.
  session["current_test"] += 1


def compile_and_execute(code_snippet):
  """Compile and executes a code snippet."""

  # Executes if the temporary folder exists.
  if Path("temporary").exists():

    # Deletes the temporary folder.
    shutil.rmtree("temporary")

  # Creates a temporary folder.
  Path("temporary").mkdir()

  # Opens the result file for writing and the Java main class parts for
  # reading.
  with open(RESULT_FILENAME, "w") as result_file, open(JAVA_MAIN_BEGINNING,
    "r") as java_main_beginning, open(JAVA_MAIN_END, "r") as java_main_end:
  
    # Joins the Java Main class parts to a complete Main class and stores it
    # in the temporary folder.
    result_file.write(java_main_beginning.read())
    result_file.write(code_snippet)
    result_file.write(java_main_end.read())


  # Initializes the compilation command.
  compilation_command = ""

  # Executes if the code is executed in a macOS environment.
  if platform.system() == MACOS_SYSTEM_NAME:

    # Updates the compilation command.
    compilation_command = MACOS_COMPILATION_COMMAND

  # Executes if the code is executed in a Linux environment.
  elif platform.system() == LINUX_SYSTEM_NAME:

    # Updates the compilation command.
    compilation_command = LINUX_COMPILATION_COMMAND

  # Executes if the code is executed in a Windows environment.
  elif platform.system() == WINDOWS_SYSTEM_NAME:

    # Updates the compilation command.
    compilation_command = WINDOWS_COMPILATION_COMMAND

  # Executes if the code is executed in an unknown environment.
  else:

    # Throws an exception.
    raise Exception(UNKNOWN_SYSTEM_MESSAGE)
    
  # Compiles the Java Main class and stores the result.
  compilation_result = subprocess.run(compilation_command + RESULT_FILENAME,
    shell=True, capture_output=True, text=True)

  # Stores the compilation errors.
  compilation_errors = compilation_result.stderr.strip()

  # Initializes the result.
  result = ""

  # Initializes the runtime errors.
  runtime_errors = ""

  # Executes if no errors were encountered during the compilation.
  if compilation_result.returncode == 0:

    # Changes directory to the temporary folder.
    os.chdir("temporary")

    # Initializes the execution command.
    execution_command = ""

    # Executes if the code is executed in a macOS environment.
    if platform.system() == MACOS_SYSTEM_NAME:

      # Updates the execution command.
      execution_command = MACOS_EXECUTION_COMMAND
    
    # Executes if the code is executed in a Linux environment.
    elif platform.system() == LINUX_SYSTEM_NAME:

      # Updates the execution command.
      execution_command = LINUX_EXECUTION_COMMAND

    # Executes if the code is executed in a Windows environment.
    elif platform.system() == WINDOWS_SYSTEM_NAME:

      # Updates the execution command.
      execution_command = WINDOWS_EXECUTION_COMMAND

    # Executes if the code is executed in an unknown environment.
    else:
      # Throws an exception.
      raise Exception(UNKNOWN_SYSTEM_MESSAGE)

    # Executes the Java Main class and stores the result.
    execution_result = subprocess.run(execution_command, shell=True,
      capture_output=True, text=True)

    # Changes directory to the parent folder.
    os.chdir("..")

    # Stores the normal execution result.
    result = execution_result.stdout.strip()

    # Stores the runtime errors.
    runtime_errors = execution_result.stderr.strip()

  # Stores the result of compiling and executing the code snippet in the
  # return value.
  return jsonify(result = result, compilation_errors = compilation_errors,
    runtime_errors = runtime_errors)

