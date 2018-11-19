# Zal


OBJECTIVE:  
To build a dockerized app with APIs for uploading and downloading files  

HOWTO:  
To build the images, run the following as root:

docker build -t file-app .  

docker run --name file-app -p 80:5000 file-app

Use a browser to perform the following:

To upload a file:
http://server/

To list contents of upload:
http://server/list/

To view the contents of uploaded files:
http://server/list/filename

To select a file to delete:
http://server/delete/

FEATURES:
Added hashing to files to detect and avoid duplication, used links for identical files with different file names

TODO:
Basic user authentication

Share nothing buddy for replication


CREDIT:
Code from http://flask.pocoo.org/docs/1.0/patterns/fileuploads/ used as initial template

https://www.pythoncentral.io/finding-duplicate-files-with-python/ for deduplication code

Dockerfile template from https://www.wintellect.com/containerize-python-app-5-minutes/
