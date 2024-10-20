import ollama
import os
import git
import shutil
import stat
import requests
import subprocess
from flask import Flask, render_template, request
from guesslang import Guess
import time

def chat(message):
    user_message = [{
    'role': 'user',
    'content': message,
    }]
    messages.append(user_message[0])
    response = ollama.chat(model="deepseek-coder", messages=messages)
    answer = response['message']['content']
    messages.append(response['message'])
    return answer

def delete_files_and_folders(folder):
    # Ensure the folder exists
    if not os.path.exists(folder):
        print(f"Folder '{folder}' does not exist.")
        return

    # Iterate over all files and folders in the directory
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        
        try:
            # Change permissions to ensure file or folder can be deleted
            os.chmod(file_path, stat.S_IWRITE)
            
            # If the file_path is a file or symlink (including symlinks to directories), delete it
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f"Deleted file or link: {file_path}")

            # If it's a directory, delete it and its contents recursively
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path, onerror=handle_remove_error)
                print(f"Deleted directory: {file_path}")

        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except PermissionError:
            print(f"Permission denied: {file_path}. Retrying with modified permissions.")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def handle_remove_error(func, path, exc_info):
    """
    Error handler for `shutil.rmtree()` to handle read-only files.
    `func` is the function that raised the error (os.unlink, os.rmdir, etc.)
    `path` is the path to the file that couldn't be removed
    `exc_info` is the exception information returned by sys.exc_info()
    """
    exc_type, exc_value, _ = exc_info
    if isinstance(exc_value, PermissionError):
        # Change the permissions to write and try again
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise

def list_files_in_directory(directory):
    paths = []
    
    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for name in dirs:
            if ".git" not in root:
                paths.append(os.path.join(root, name))  # Add directory path to the list
        for name in files:
            if ".git" not in root:
                paths.append(os.path.join(root, name))  # Add file path to the list
    
    return paths

def correct(multiple):
    error_list = fixed_list = []
    count = 0
    json = ""
    list_files=list_files_in_directory(r"C:\Users\iyerp\Downloads\Hackathon\input")
    try:
        list_files.remove(r"C:\Users\iyerp\Downloads\Hackathon\input\.dccache")
    except:
        pass
    for path in list_files:
        count += 1
        if not multiple:
            os.system(r'snyk code test "C:\Users\iyerp\Downloads\Hackathon\input" --json-file-output="C:\Users\iyerp\Downloads\Hackathon\input\corrections.json"')
            try:
                fh2 = open(r"C:\Users\iyerp\Downloads\Hackathon\input\corrections.json")
                json = fh2.read(fh2)
                print("Snyk Analysis Successful")
                fh2.close()
            except:
                pass
        try:
            fh = open(f"{path}")
            code = fh.read()
            print("read out\n",f"{path}\n",code)
            errors = chat("Source Code: {}\nPlease find any errors with this. Use the following static analysis for reference: {}\n Give me only a list of vulnerabilities and errors.".format(code,json))
            if not multiple:
                fixed = chat("Source Code: {}\nPlease give me the correct code of this. Use the following static analysis for reference: {}\n Give me only the corrected code. Do not give me the errors. Concise, brief, no formatting, no intro, no conclusion. Only code.".format(code,json))
            error_list.append(errors)
            fixed_list.append(fixed)
            fh.close()
        except:
            pass
        print("Completion: {}".format(count/len(list_files)*100))
    folder = r"C:\Users\iyerp\Downloads\Hackathon\input"
    delete_files_and_folders(folder)
    return error_list,fixed_list

def write_to_file(code):
    lang = guess.language_name(code)
    dictionary = {
    'Assembly': '.asm',
    'Batchfile': '.bat',
    'C': '.c',
    'C#': '.cs',
    'C++': '.cpp',
    'Clojure': '.clj',
    'CMake': '.cmake',
    'COBOL': '.cob',
    'CoffeeScript': '.coffee',
    'CSS': '.css',
    'CSV': '.csv',
    'Dart': '.dart',
    'DM': '.dm',
    'Elixir': '.ex',
    'Erlang': '.erl',
    'Fortran': '.f90',
    'Go': '.go',
    'Groovy': '.groovy',
    'Haskell': '.hs',
    'HTML': '.html',
    'INI': '.ini',
    'Java': '.java',
    'JavaScript': '.js',
    'JSON': '.json',
    'Julia': '.jl',
    'Kotlin': '.kt',
    'Lisp': '.lisp',
    'Lua': '.lua',
    'Markdown': '.md',
    'Matlab': '.m',
    'Objective-C': '.m',
    'OCaml': '.ml',
    'Pascal': '.pas',
    'Perl': '.pl',
    'PHP': '.php',
    'PowerShell': '.ps1',
    'Prolog': '.pl',
    'Python': '.py',
    'R': '.r',
    'Ruby': '.rb',
    'Rust': '.rs',
    'Scala': '.scala',
    'Shell': '.sh',
    'SQL': '.sql',
    'Swift': '.swift',
    'TeX': '.tex',
    'TOML': '.toml',
    'TypeScript': '.ts',
    'Verilog': '.v',
    'Visual Basic': '.vb',
    'XML': '.xml',
    'YAML': '.yaml'
}

    ext = dictionary[lang]
    fh = open(r"C:\Users\iyerp\Downloads\Hackathon\input\text{}".format(ext),"w")
    fh.write(code)
    fh.close()

def move_files_and_delete_folders(main_directory):
    # Loop through the subdirectories and files in the main directory
    for root, dirs, files in os.walk(main_directory, topdown=False):
        # Move all files to the main directory
        for file in files:
            if ".git" not in root:
                file_path = os.path.join(root, file)
                new_path = os.path.join(main_directory, file)
                shutil.move(file_path, new_path)
                print(f"Moved: {file_path} -> {new_path}")
            
        # After moving files, delete the empty directories
        for dir in dirs:
            if ".git" not in root:
                dir_path = os.path.join(root, dir)
                try:
                    os.rmdir(dir_path)  # Will only delete if empty
                    print(f"Deleted folder: {dir_path}")
                except OSError as e:
                    print(f"Error: {dir_path} not empty or could not be deleted - {e}")
                    
def clone_repository(repo_url, clone_dir=r"C:\Users\iyerp\Downloads\Hackathon\input"):
    folder = r"C:\Users\iyerp\Downloads\Hackathon\input"
    delete_files_and_folders(folder)
    if os.path.exists(clone_dir):
        os.rmdir(clone_dir)
    os.makedirs(clone_dir)
    git.Repo.clone_from(repo_url, clone_dir)
    move_files_and_delete_folders(folder)
    return clone_dir

import pyuac
messages= []
ollama.pull('deepseek-coder')
guess = Guess()
app = Flask(__name__)

# Route for the index page
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/choice", methods=["GET", "POST"])
def choice():
    return render_template("choice.html")

@app.route("/source", methods=["GET", "POST"])
def source():
    if request.method == "POST":
        # Get the input from the text box
        user_input = request.form["input_text"]
        write_to_file(user_input)
        corrections, corrected = correct(multiple = False)
        prob = guess.probabilities(corrected[0])
        if prob[0][1] < 0 or guess.language_name(corrected[0]) == "Markdown":
            corrected = ["Not Available"]
        print("Results")
        
        # Process the input to generate two outputs (customize this part as needed)

        output_1 = f"{corrections[0]}"
        output_2 = f"{corrected[0]}"
        
        # Render the template with both outputs
        return render_template("source.html",show_result="True",output_1=output_1, output_2=output_2)
    
    # GET method - just render the page with no outputs
    return render_template("source.html",show_result="False")

@app.route("/gitpage", methods=["GET", "POST"])
def gitpage():
    if request.method == "POST":
        # Get the input from the text box
        user_input = request.form["input_text"]
        clone_repository(user_input)
        path_list = list_files_in_directory(r"C:\Users\iyerp\Downloads\Hackathon\input")
        corrections, corrected = correct(multiple = True)        
        # Process the input to generate two outputs (customize this part as needed)
        i = 0
        output_1=""
        for path in path_list:
            filename = os.path.basename(path)
            if i < len(corrections):
                output_1 = output_1 + "{}: \n {}".format(filename, corrections[i])
            else:
                output_1 = output_1 + ""
            i += 1
        output_2 = "Not Applicable"
        
        # Render the template with both outputs
        return render_template("source.html",show_result="True",output_1=output_1, output_2=output_2)
    
    # GET method - just render the page with no outputs
    return render_template("source.html",show_result="False")


if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        pyuac.runAsAdmin()
    else:        
        app.run(debug=True) # Already an admin here.
