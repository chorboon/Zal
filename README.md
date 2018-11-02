# Zal

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

TODO:

Add hashing to files to detect and avoid duplication
