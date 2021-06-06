import os
from flask import Flask
from . import database
from . import survey_handler
from . import code_snippet_handler


# A Flask application factory.
def create_app(test_configuration = None):

  # Creates the application with configuration files relative to the instance
  # folder.
  application = Flask(__name__, instance_relative_config = True)

  # Sets the application default configuration.
  application.config.from_mapping(
    
    # Sets the secret key.
    SECRET_KEY='dev',
    
    # Sets the database path.
    DATABASE=os.path.join(application.instance_path, 'code_comparator.sqlite'),
  )

  # Executes if no test configuration is provided.
  if test_configuration is None:

    # Reads the configuration from a file in the instance folder.
    application.config.from_pyfile('configuration.py', silent=True)

  # Executes if a test configuration is provided.
  else:

    # Configures the application from the provided test configuration.
    application.config.from_mapping(test_configuration)

  # Creates a try block.
  try:

    # Creates the instance path.
    os.makedirs(application.instance_path)

  # Captures operating system exceptions.
  except OSError:

    # Executes a null statement.
    pass

  # Registers the database with the application.
  database.initialize_application(application)

  # Registers the survey handler blueprint.
  application.register_blueprint(survey_handler.blueprint)

  # Registers the code snippet handler blueprint.
  application.register_blueprint(code_snippet_handler.blueprint)

  # Registers the index view function for the / URL.
  application.add_url_rule('/', endpoint='index')


  # Returns the created application to the caller.
  return application