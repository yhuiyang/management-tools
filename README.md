Google Play Games Services Management Tools on Google App Engine
================================================================

Google has provided management tools for your play games service
project. With the tools, you can hide specific users (tester,
cheater...) from leaderboards, and test other functions related 
to achievements and leaderboards.
These tools are web apps, you need to host them somewhere. Host
on localhost is possible but not safe. This project helps to host
these web apps on Google App Engine.


Deploy
------
You need to have google account which can create project on GAE.
In the top directory of this project, type: (Only test on Linux)

$ appcfg.py update --oauth2 -A <replace-with-your-app-name> app.yaml


Link app
--------
In your game project on Google play Developer console, create a linked
web app, and type in 'gpgmgr.<replace-with-your-app-name>.appspot.com'
in the 'Launch URL' field.
Write down the 'app id', 'client id', and one of your 'leaderboard id'
for later use.


Run Tools
---------
Launch browser to http://gpgmgr.<replace-with-your-app-name>.appspot.com.
Click 'Show form' button and fill those data into the form, then click
'New App' button to create one app row in below App list table.

