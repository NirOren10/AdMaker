MentaList
#### Video Demo:  https://youtu.be/190bE99eTcM
================================
#### Description:
This is a web based application built using Flask, Python, CSS, HTML and JavaScript. The purpose of this website is to keep track of mental health, help improve it, and connect users to other users on the website.
This app features:

- a calendar where the user inputs how their day is from 1-5 and a short description, and can see all his data on an interactive calendar.

- Chat service between users.

- Locator of users around you.

- Discover page where the user can find parks, hikes and activities in the area, and excercise breathing excercises for better mental health.

####Discover:
There is a discover page, which shows parks hikes and activities in the area, and breathing excercises. 
The inbox features an inbox,
of chats between users. 

####login + register:
The login and register feature login and register, which contact the SQLite Data base, in table users. in register they need a name, username, password, password confirmation, gender, state, city and phone numner.
the register has features to insure there is no username duplicates, all fields are filled and password and password confirmation are the same

####connect:
connect can show people in the area with a chat button to chat with them. it shows all people in the state, their name, username, phone number and a chat button, which directs the user to message.html

####index:
this is the interactive calendar that shows all the day data(description + value from 1-5) the user inputs. if clicks on a day with a value/color, the user can
see the description they inputed. In the Index the user can go to next and previous months, to see all their data

####inbox:
in the inbox the user will find all their messages, with the username of the sender, title, message and time received, and on the top left will find a new message button where they can send a new message with another user's username
there are three SQLite data bases, users: info about users:

####databases:
users:
username, hash, name, gender, city, state, phone

days: days of the users and their description:
userID, year, month, day, day_value, description

messages: all the messages:
senderID, receiverID, title, message, year, month, day, hour, minute, second, date


This app's purpose is to keep trakc of mental health data about users' days, their description, and their value from 1-5 to show upwards or downwards trends, to help them discover activities in the area, and a chatting service between the users to allow them to connect with people and support each other
I think this app is a mini platform that can connect the users and influence them for the better, show them places where they can take care of themselves and their mental health, and keep track of 'themselves'.# AdMaker
