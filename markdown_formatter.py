#!/usr/bin/env python3
"""
Module providing automatically formatting functionality to markdown files 
following the Microsoft Learn Guidelines
"""
import os
import argparse

def main():
    """Main program function defined below"""
    # get input arguments
    in_arg = get_input_args()

    tutorials = get_tutorials_exercises_paths(in_arg.dir)
    # iterate over the files to validate content
    for tutorial_folder_name, tutorial_exercises in tutorials.items():
        for tutorial_exercise in tutorial_exercises:
            markdown_file_path = os.path.join(
                in_arg.dir,
                tutorial_folder_name + '/includes/' + tutorial_exercise)
            if in_arg.func == 'first_two_lines':
                format_first_two_lines(markdown_file_path)


# Helper Functions

def get_tutorials_exercises_paths(root_path : str) -> dict:
    """
    Function to compile a dictionary of tutorial exercises with 
    the tutorial folder name as key
    """
    tutorials = {}
    # get tutorial folders
    for item in os.listdir(root_path):
        if os.path.isdir(os.path.join(root_path, item)):
            tutorials[item] = []

    # get tutorial exercises (includes folder content)
    for tutorial in tutorials.keys():
        for item in os.listdir(os.path.join(root_path, tutorial + '/includes/')):
            tutorials[tutorial].append(item)

    return tutorials

def format_first_two_lines(filepath: str) -> None:
    """Function that formats the first 2 lines in a tutorial exercise"""
    # read the file data and store the first two lines content
    with open(filepath, 'r', encoding="utf-8") as file:
        filedata = file.read()
        # check if if the file length is less than two sentences
        if len(filedata.split('\n')) < 2:
            return
        first_line, second_line = filedata.split('\n')[:2]
        

    # check if first line doesn't contains the correct sentence
    if "<!-- markdownlint-disable MD041 -->" not in first_line:
        filedata = '<!-- markdownlint-disable MD041 -->\n\n' + filedata
        # Write the file out again
        with open(filepath, 'w', encoding="utf-8") as file:
            file.write(filedata)
    # check if second line is not empty
    elif second_line not in ['\n', '\r\n', '', ' ']:
        filedata = filedata.replace('<!-- markdownlint-disable MD041 -->', 
                                    '<!-- markdownlint-disable MD041 -->\n')
        # Write the file out again
        with open(filepath, 'w', encoding="utf-8") as file:
            file.write(filedata)

def get_input_args():
    """
    Retrieves and parses the 2 command line arguments provided by the user when
    they run the program from a terminal window. This function uses Python's 
    argparse module to created and defined these 2 command line arguments. If 
    the user fails to provide some or all of the 2 arguments, then the default 
    values are used for the missing arguments. 
    Command Line Arguments:
      1. Tutorials Path as --dir with default value './docs/dev/tutorials/'
      2. Function to be executed as --func with default value 'first_two_lines'
    This function returns these arguments as an ArgumentParser object.
    Parameters:
     None - simply using argparse module to create & store command line arguments
    Returns:
     parse_args() -data structure that stores the command line arguments object  
    """
    # Parse using ArgumentParser
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--dir', type = str, default = './docs/dev/tutorials/',
                    help = 'path to the root directory', required=True)

    parser.add_argument('-f', '--func', type = str, choices=['first_two_lines'],
                        default = 'first_two_lines', help = 'function to be executed',
                        required = True)

    return parser.parse_args()


# Call to main function to run the program
if __name__ == "__main__":
    main()
