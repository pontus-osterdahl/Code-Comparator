// Executes when the web page is loaded.
document.addEventListener("DOMContentLoaded", function()
{
  // Selects the editor element.
  var editor = ace.edit("code_snippet_area");
  
  // Sets the editor theme.
  editor.setTheme("ace/theme/xcode");
  
  // Sets the editor language.
  editor.session.setMode("ace/mode/java");

  // Executes when the execute button is clicked.
  execute_button.addEventListener("click", function()
  {
    // Retrieves the code snippet from the editor.
    var codeSnippet = editor.getValue();

    // Creates an AJAX request.
    var request = new XMLHttpRequest();

    // Configures the request as POST with URL and asynchronous
    // operation.
    request.open("POST", "/code_snippet_handler/comprehensibility_test", true);

    // Configures the request content type.
    request.setRequestHeader('content-type',
      'application/x-www-form-urlencoded;charset=UTF-8');

    // Sends the request including the code snippet.
    request.send("code_snippet_area=" + encodeURIComponent(codeSnippet));

    // Executes when the request response is received.
    request.onload = function()
    {
      // Parses the response data.
      var parsedResponse = JSON.parse(request.response)

      // Finds the result area.
      var resultArea = document.getElementById("result_area");

      // Retrieves the execution result from the response.
      var result = parsedResponse.result;

      // Retrieves the compilation errors from the response.
      var compilationErrors = parsedResponse.compilation_errors;

      // Retrieves the runtime errors from the response.
      var runtimeErrors = parsedResponse.runtime_errors;

      // Stores the combined result.
      var combinedResult = "";
      
      // Executes if an execution result exists.
      if (result)
      {
        // Adds the execution result to the combined result.
        combinedResult += (result + "\n\n");
      }

      // Executes if compilation errors exists.
      if (compilationErrors)
      {
        // Adds the compilation errors to the combined result.
        combinedResult += ("Compilation errors\n------------------\n" +
          compilationErrors + "\n\n");
      }

      // Executes if runtime errors exists.
      if (runtimeErrors)
      {
        // Adds the runtime errors to the combined result.
        combinedResult += ("Runtime errors\n--------------\n" + runtimeErrors);
      }

      // Updates the result area with the combined result.
      resultArea.innerHTML = combinedResult;
    }
  });

  // Executes when the finish button is clicked.
  finish_button.addEventListener("click", function()
  {
    // Retrieves the code snippet from the editor.
    var codeSnippet = editor.getValue();

    // Creates an AJAX request.
    var request = new XMLHttpRequest();

    // Configures the request as POST with URL and asynchronous
    // operation.
    request.open("POST", "/code_snippet_handler/comprehensibility_test", true);

    // Configures the request content type.
    request.setRequestHeader('content-type',
      'application/x-www-form-urlencoded;charset=UTF-8');

    // Sends the request including the code snippet and a finish indicator set
    // to true.
    request.send("code_snippet_area=" + encodeURIComponent(codeSnippet) +
      "&finish=true");

    // Executes when the request response is received.
    request.onload = function()
    {
      // Parses the response data.
      var parsedResponse = JSON.parse(request.response);

      // Updates the code snippet editor with the code snippet from the
      // response.
      editor.setValue(parsedResponse.code_snippet);

      // Resets the code snippet editor selection.
      editor.clearSelection();

      // Stores the information area.
      var informationArea = document.getElementById("information_area");

      // Updates the information area with the information from the response.
      informationArea.innerHTML = parsedResponse.information;

      // Stores the result area.
      var resultArea = document.getElementById("result_area");

      // Clears the result area .
      resultArea.innerHTML = "";

      // Executes if all comprehensibility tests are finished.
      if (parsedResponse.finito)
      {
        // Disables the execute button.
        document.getElementById("execute_button").disabled = true;

        // Disables the finish button.
        document.getElementById("finish_button").disabled = true;
      }
      
    }
  });
  
});