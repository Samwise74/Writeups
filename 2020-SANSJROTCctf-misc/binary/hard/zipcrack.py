import zipfile
import itertools
import time
import base64


# important variables
# zipfilepath = path to zip file
# password_file = path to word list
zipfilepath = '/path/to/c1000.zip'
password_file = '/path/to/rockyou.txt'


# Function for extracting zip files to test if the password works
def extractFile(zip_file, password):
    try:
        zip_file.extractall(pwd=password)
        return True
    except KeyboardInterrupt:
        exit(0)
    except Exception:
        pass


zip_file = zipfile.ZipFile(zipfilepath)

with open(password_file, "r") as pass_file:
    try:
        for password in pass_file:
            print('trying password %s' % password.strip())
            password = base64.b64encode(password.strip().encode())
            if extractFile(zip_file, password):
                print('Password found: %s' % password)
		print('Files extracted')
                exit(0)
    except UnicodeDecodeError:
        pass

print('Password not found.')
