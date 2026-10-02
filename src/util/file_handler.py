import json
import os
import datetime
import re
import shutil

def generate_timestamp():
    now = datetime.datetime.now()
    date = now.strftime("%Y_%m_%d")  # Formats the date as
    time = now.strftime("%H%M%S")   
    return f"{date}_{time}"



def setup_output_dir(model, job, session, temperature, version, module_path, prompt_type, run_number, no_rag=False):
    session_name = f"session{session}_temp{temperature}"
    
    try:
        is_temp1 = float(temperature) == 1.0
    except (ValueError, TypeError):
        is_temp1 = False

    if no_rag:
        base_dir = "./output/no_rag/temp1" if is_temp1 else "./output/no_rag"
    else:
        base_dir = "./output/temp1" if is_temp1 else "./output"
    
    # Format: base_dir/model/module_path/prompt_type/runN
    output_dir = os.path.join(
        base_dir, model, module_path, prompt_type, f"run{run_number}")
    
    # Create the directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Return the absolute path of the output directory and session name
    return output_dir, session_name

def pytest_runner_set_up(modules_under_test_paths, original_test_paths, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    if isinstance(modules_under_test_paths, str):
        modules_under_test_paths = [modules_under_test_paths]
    elif modules_under_test_paths is None:
        modules_under_test_paths = []

    if isinstance(original_test_paths, str):
        original_test_paths = [original_test_paths]
    elif original_test_paths is None:
        original_test_paths = []

    for module_path in modules_under_test_paths:
        if os.path.isfile(module_path):
            target_path = os.path.join(output_dir, os.path.basename(module_path))
            shutil.copy(module_path, target_path)
            print(f"Copied {module_path} to {target_path}")
        elif os.path.isdir(module_path):
            raise IsADirectoryError(f"Expected a file but got a directory: {module_path}")
        else:
            raise FileNotFoundError(f"Module path does not exist: {module_path}")

    for test_path in original_test_paths:
        if os.path.isfile(test_path):
            test_target_path = os.path.join(output_dir, os.path.basename(test_path))
            shutil.copy(test_path, test_target_path)
            print(f"Copied {test_path} to {test_target_path}")
        elif os.path.isdir(test_path):
            raise IsADirectoryError(f"Expected a file but got a directory: {test_path}")
        else:
            raise FileNotFoundError(f"Test path does not exist: {test_path}")

    

####################################################################################################
# Json file operations
####################################################################################################

def create_json_file(directory, file_name, data): 
    os.makedirs(directory, exist_ok=True)
    file_name = directory + file_name
    with open(file_name + ".json", 'w') as file:
        json.dump(data, file, indent=4)
    return file_name

def append_json_file(file_name, data):
    with open(file_name + ".json" , 'r') as file:
        file_data = json.load(file)
    file_data.append(data)
    with open(file_name + ".json", 'w') as file:
        json.dump(file_data, file, indent=4)
    return file_name

def read_json_file(file_name):
    with open(file_name + ".json", 'r') as file:
        data = json.load(file)
    return data

####################################################################################################
# Text file operations
####################################################################################################

def create_text_file(directory, file_path, data):
    os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory, file_path)
    print("Saving text file in: ",file_path)
    with open(file_path, 'w') as file:
        file.write(data +"\n")
    return file_path

def append_text_file(file_path, data):
    with open(file_path, 'a') as file:
        file.write(data + "\n")
    return file_path

def read_text_file(file_name):
    with open(file_name, 'r') as file:
        data = file.read()
    return data



def get_log_imports_template(system_prompt, user_prompt, response, post_process_response):
    import_log_template= f''' 
    ###########################################################
    # Imports 
    ***********************************************************
    \n
    System promp: \n
    {system_prompt}\n
    User prompt:\n
    {user_prompt}
    \n
    ***********************************************************
    * Model Response 
    ***********************************************************
    response:
    {response} \n\n
    After regex:
    {post_process_response} 
    ###########################################################
    \n\n  '''
     
    return import_log_template

def get_log_response_template(system_prompt, user_prompt_2, response, post_process_response, counter=0):
    if counter == 0:
        counter = "No counter provided"       

    refactoring_log_template = f''' 
    #######################################################################################
    # Test case - {counter}
    ***********************************************************\n
    System promp: \n
    {system_prompt}\n
    ***********************************************************\n
    User prompt:\n
    {user_prompt_2}
    \n
    ***********************************************************
    * Model Response 
    ***********************************************************
    Response: 
    {response} \n\n
    ******************************************\n
    Post processing: 
    {post_process_response} \n 

    ########################################################################################\n\n  '''

    return refactoring_log_template

def get_log_summary_template(function_name, user_prompt, response):
    summary_log_template= f''' 
    ###########################################################
    # Function: {function_name} 
    ***********************************************************
    {user_prompt}
    ***********************************************************
    * Summary 
    ***********************************************************
    {response} 
    ###########################################################\n\n  '''
    return summary_log_template
            



####################################################################################################
# Create Python file
####################################################################################################

#Creates a python file and insert the imports
def create_refactored_python_file(directory, test_paths, code, version):
    # Allow test_paths to be either a single path (str) or list of paths
    if isinstance(test_paths, str):
        test_paths = [test_paths]

    refactored_files = []

    for test_path in test_paths:
        base_name = os.path.basename(test_path)
        name, extension = os.path.splitext(base_name)
        new_test_file_path = f"{name}_{version}_refactored.py"
    
        # Create the directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        print("Create python file in directory: ", directory)
        # Construct the full file path
        file_path = os.path.join(directory, new_test_file_path)
        print("Saving file in: ", file_path)
        
        # Write the code to the Python file
        with open(file_path, 'w') as file:
            file.write(code + "\n\n")

        refactored_files.append(file_path)

    # If only one file refactored, return just that path, else return list
    if len(refactored_files) == 1:
        return refactored_files[0]
    else:
        return refactored_files

#Creates a python file and insert the imports
def create_python_file(directory, file_path, code):
    # Check if the provided file_name ends with .py
    if not file_path.endswith('.py'):
        file_path += '.py'
    
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Construct the full file path
    file_path = os.path.join(directory, file_path)
    
    # Write the code to the Python file
    with open(file_path, 'w') as file:
        file.write(code + "\n\n")
    
    return file_path
    
def append_test_case(file_paths, test_case):
    if isinstance(file_paths, str):
        file_paths = [file_paths]

    updated_paths = []
    for file_path in file_paths:
        with open(file_path, 'a') as file:
            file.write(test_case + "\n\n")
        updated_paths.append(file_path)

    return updated_paths

def read_python_file(file_name):
    with open(file_name, 'r') as file:
        data = file.read()
    return data

def get_modules_under_test(paths):
    module_under_test = []

    for path in paths:
        file = read_python_file(path)
        module_under_test.append(file)

    return module_under_test
    
