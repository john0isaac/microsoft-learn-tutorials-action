#!/usr/bin/env python3
"""
Module providing automatically formatting functionality to markdown files 
following the Microsoft Learn Guidelines
"""
import os
import argparse
import logging
import re

def main():
    """Main program function defined below"""
    # initialize logger
    logger = logging.getLogger()

    # get input arguments
    in_arg = get_input_args()

    # define list of folder to skip
    pass_list = ['acs-to-teams-meeting',
                 'aml-powerapps-powerautomate',
                 'openai-acs-msgraph']

    logger.info('Reading the tutorial exercises')
    tutorials = get_tutorials_exercises_paths(in_arg.dir, pass_list)

    # iterate over the files to validate content
    for tutorial_folder_name, tutorial_exercises in tutorials.items():
        for tutorial_exercise in tutorial_exercises:
            markdown_file_path = os.path.join(
                in_arg.dir,
                tutorial_folder_name + '/includes/' + tutorial_exercise)
            if "first_two_lines" in in_arg.func:
                try:
                    logger.info('Formatting the first two lines')
                    format_first_two_lines(markdown_file_path)
                except FileNotFoundError:
                    logger.error('Failed to format the first two lines of %s', markdown_file_path)
            elif "add_empty_last_line" in in_arg.func:
                try:
                    logger.info('Adding empty last line')
                    add_empty_last_line(markdown_file_path)
                except FileNotFoundError:
                    logger.error('Failed to add an empty line to %s', markdown_file_path)
            elif "replace_all_with_select" in in_arg.func:
                try:
                    logger.info('Replacing with Select')
                    replace_all_with_select(markdown_file_path)
                except FileNotFoundError:
                    logger.error('Failed to replace with select in %s', markdown_file_path)
            elif "remove_links_locale" in in_arg.func:
                try:
                    logger.info('Removing links locale')
                    remove_links_locale(markdown_file_path)
                except FileNotFoundError:
                    logger.error('Failed to remove locale from links in %s', markdown_file_path)
            elif "remove_relative_links" in in_arg.func:
                try:
                    logger.info('Removing relative links')
                    remove_relative_links(markdown_file_path)
                except FileNotFoundError:
                    logger.error('Failed to remove relative links in %s', markdown_file_path)
            elif "add_carriage_return" in in_arg.func:
                try:
                    logger.info('Adding carriage return')
                    add_carriage_return(markdown_file_path)
                except FileNotFoundError:
                    logger.error('Failed to add carriage return in %s', markdown_file_path)

# Helper Functions

def get_tutorials_exercises_paths(root_path : str, pass_list : list) -> dict:
    """
    Function to compile a dictionary of tutorial exercises with 
    the tutorial folder name as key
    """
    tutorials = {}
    # get tutorial folders
    for item in os.listdir(root_path):
        if os.path.isdir(os.path.join(root_path, item)):
            if item not in pass_list:
                tutorials[item] = []

    # get tutorial exercises (includes folder content)
    for tutorial in tutorials.keys():
        for item in os.listdir(os.path.join(root_path, tutorial + '/includes/')):
            tutorials[tutorial].append(item)

    return tutorials

def format_first_two_lines(filepath: str) -> None:
    """Function that formats the first 2 lines in a tutorial exercise"""
    # read the file data, skip if file is small, and store the first two lines content
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

def add_empty_last_line(filepath: str) -> None:
    """Function that formats the adds an empty line to the end of tutorial exercise"""
    # read the file data, skip if file is small, and store the last line
    with open(filepath, 'r', encoding="utf-8") as file:
        filedata = file.read()
        # check if if the file length is less than two sentences
        if len(filedata.split('\n')) < 2:
            return
        last_line = filedata.split('\n')[-1]

    # check if first line doesn't contains the correct sentence
    if last_line not in ['\n', '\r\n', '', ' ']:
        filedata = filedata + '\n'
        # Write the file out again
        with open(filepath, 'w', encoding="utf-8") as file:
            file.write(filedata)

def replace_all_with_select(filepath: str) -> None:
    """Function that replaces words "choose" and "click" with select"""
    # read the file data and skip if file is small
    with open(filepath, 'r', encoding="utf-8") as file:
        filedata = file.read()
        # check if if the file length is less than two sentences
        if len(filedata.split('\n')) < 2:
            return
    original_filedata = filedata
    try:
        # starts with uppercase
        filedata = filedata.replace(' Choose ', ' Select ')
        filedata = filedata.replace(' Click ', ' Select ')
        # starts with lowercase
        filedata = filedata.replace(' choose ', ' select ')
        filedata = filedata.replace(' click ', ' select ')
        # ends with ing
        filedata = filedata.replace('Choosing', 'Selecting')
        filedata = filedata.replace('Clicking', 'Selecting')
    finally:
        if filedata != original_filedata:
            # Write the file out again
            with open(filepath, 'w', encoding="utf-8") as file:
                file.write(filedata)

def remove_links_locale(filepath: str) -> None:
    """Function that replaces the country locale with a forward slash"""
    # read the file data and skip if file is small
    with open(filepath, 'r', encoding="utf-8") as file:
        filedata = file.read()
        # check if if the file length is less than two sentences
        if len(filedata.split('\n')) < 2:
            return

    original_filedata = filedata
    # match the following pattern / two small characters a ~ z - two small characters a ~ z /
    filedata = re.sub(r'\/[a-z]{2}-[a-z]{2}\/', '/', filedata)

    if filedata != original_filedata:
        # Write the file out again
        with open(filepath, 'w', encoding="utf-8") as file:
            file.write(filedata)

def remove_relative_links(filepath: str) -> None:
    """Function that replaces relative links learn.microsoft.com/ with a forward slash"""
    # read the file data and skip if file is small
    with open(filepath, 'r', encoding="utf-8") as file:
        filedata = file.read()
        # check if if the file length is less than two sentences
        if len(filedata.split('\n')) < 2:
            return

    original_filedata = filedata
    # match the following pattern http:// or https:// or nothing followed by learn.microsoft.com
    filedata = re.sub(r'(https?:\/\/)?(learn\.microsoft\.com)\/', '/', filedata)

    if filedata != original_filedata:
        # Write the file out again
        with open(filepath, 'w', encoding="utf-8") as file:
            file.write(filedata)

def add_carriage_return(filepath: str) -> None:
    """Function that adds carriage return before and after lines"""
    # read the file data and skip if file is small
    with open(filepath, 'r', encoding="utf-8") as file:
        filelines = file.readlines()
        filedata = ''.join(filelines)
        # check if if the file length is less than two sentences
        if len(filelines) < 2:
            return

    original_filelines = filelines
    new_filelines = filelines

    if ":::image" in filedata:
        new_filelines = images_carriage_return(new_filelines)
    if ">" in filedata:
        new_filelines = blockquote_carriage_return(new_filelines)

    if new_filelines != original_filelines:
        # Write the file out again
        with open(filepath, 'w', encoding="utf-8") as file:
            for line in new_filelines:
                file.write(line)

def images_carriage_return(original_filelines: list) -> list:
    """ Function that checks images line and add blank lines before and after them """
    new_filelines = []
    # check each line in the file lines
    for i, line in enumerate(original_filelines):
        # check if the line check image and add the original line data if no image
        if ':::' in line:
            # check the line before the image and add new line if not blank
            if original_filelines[i-1].strip() != '':
                new_filelines.append('\n')

            new_filelines.append(line)

            # check the line after the image and add new line if not blank
            if original_filelines[i+1].strip() != '':
                new_filelines.append('\n')
        else:
            new_filelines.append(line)
    return new_filelines

def blockquote_carriage_return(original_filelines: list) -> list:
    """ Function that checks block quotes and add blank lines before and after them """
    new_filelines = []
    # check each line in the file lines
    for i, line in enumerate(original_filelines):
        # check if the line has blockquote and add the original line data if no blockquote
        if '>' in line:
            # check the line before the blockquote and add new line if not blank
            if original_filelines[i-1].strip() != '' and '>' not in original_filelines[i-1] and '<!-- markdownlint-disable MD041 -->' not in line:
                new_filelines.append('\n')

            new_filelines.append(line)

            # check the line after the blockquote and add new line if not blank
            if original_filelines[i+1].strip() != '' and '>' not in original_filelines[i+1] and '<!-- markdownlint-disable MD041 -->' not in line:
                new_filelines.append('\n')
        else:
            new_filelines.append(line)
    return new_filelines

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

    parser.add_argument('-f', '--func', type = str, required = True,
                        help = 'function to be executed',
                        choices=['first_two_lines',
                                 'add_empty_last_line',
                                 'replace_all_with_select',
                                 'remove_links_locale',
                                 'remove_relative_links',
                                 'add_carriage_return'
                                 ])

    return parser.parse_args()


# Call to main function to run the program
if __name__ == "__main__":
    main()
