To run the website, first run python3 server.py. This will activate the restful API that works with the SQLite database and gives infromation to the Vue app.

After this, open a new terminal and move into the vue-app directory and run npm run serve. This will run the Vue app.

The Flask server runs on localhost:5000 and the vue-app runs on localhost:8080 on my computer. If your Flask server is runing on a different port, just change the fetch requests on the Vue app to whatever port it is on.

NOTE:
This contains all of the files except for the node modules. There were over 26,000 files in the folder which made it almost
impossible for my computer to upload it. Node modules can be downloaded as needed. If you have further questions email me
at ashton.winters@yale.edu.
