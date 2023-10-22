import os
import string

tutorials = {}

def format_first_two_lines(filepath: string) -> None:
    """Function that formats the first 2 lines in a tutorial exercise"""
    with open(filepath, 'r', encoding="utf-8") as file:
        filedata = file.read()
        line1, line2 = filedata.split('\n')[:2]

    if "<!-- markdownlint-disable MD041 -->" not in line1:
        filedata = '<!-- markdownlint-disable MD041 -->\n\n' + filedata
        # Write the file out again
        with open(filepath, 'w', encoding="utf-8") as file:
            file.write(filedata)
    elif line2 not in ['\n', '\r\n', '', ' ']:
        filedata = filedata.replace('<!-- markdownlint-disable MD041 -->', 
                                    '<!-- markdownlint-disable MD041 -->\n')
        # Write the file out again
        with open(filepath, 'w', encoding="utf-8") as file:
            file.write(filedata)

# get tutorial folders
path = './docs/dev/tutorials/'
for item in os.listdir(path):
    if os.path.isdir(os.path.join(path, item)):
        tutorials[item] = []


# get tutorial exercises (includes folder content)
for tutorial in tutorials.keys():
    for item in os.listdir(os.path.join(path, tutorial + '/includes/')):
        tutorials[tutorial].append(item)


# iterate over the files to validate content
for tutorial_folder_name, tutorial_exercises in tutorials.items():
    for tutorial_exercise in tutorial_exercises:
        markdown_file_path = os.path.join(path, tutorial_folder_name+ '/includes/'+tutorial_exercise)
        format_first_two_lines(markdown_file_path)
        