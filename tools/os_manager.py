import os
from requests import get

def get_public_ip():
    ip = get('https://api.ipify.org').text
    return ip

def file_tree(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

def shutdown(debug=False):
    if not debug:
        os.system("shutdown -h now")
    else:
        print("""------------------------------------------------
-------  System Shutdown  ----------------------
------------------------------------------------""")
