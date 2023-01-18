import os
from subprocess import call 

if __name__ == '__main__':
    sep = os.path.sep
    call(['python3', f'views{sep}menu.py'])