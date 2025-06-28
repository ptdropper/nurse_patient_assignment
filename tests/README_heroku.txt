heroku readme

# Heroku Deployment Instructions
1. set a new tag for the current commit
2. call generate_version.py
3. verify the file version.txt is updated
4. commit the changes to version.txt
5. push the changes to the remote repository
6. deploy to Heroku as shown below

use github to push up the remote repository

open a terminal and run the following commands:
heroku login
    manually launch the browser and login
    git push heroku master
    from herku dashboard, open the app in the browser to test

