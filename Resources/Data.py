"""
I used to find myself copy/pasting these two commands so much that I ended up putting them in a separate file that I just import.
"""

import json

# Its uh... its a function that saves data. Yeah.
def save_data(file, data):
    # Open a file. Still with me?
    with open(file, 'w+') as save_file:
        # Now, we are going to *attempt*
        try:
            # to save the data. to the file we opened.
            save_file.write(json.dumps(data, indent = 2, sort_keys = True))
        except error as e:
            # OTHERWISE, if we fail. Say that we failed. oops
            print('Could Not Save: {}'.format(e))

# Ok now things get crazy. We are gonna *load* the file now.
def load_data(file):
    # Open the file
    with open(file, 'r') as load_file:
        # Load it. Poggers.
        return json.loads(load_file.read())
