# IS211_Project
IS211 Course Project - Blog Application

Blogger is the cleverly titled blogging web application that allows multiple users to post their thoughts and ideas for the world to read. The root path presents users with a home page that displays all posts in reverse chronological order, and gives the option to register or log in. Registered users, once logged in, are taken to a dashboard page that allows them to create new posts, as well as edit or delete existing posts. A simple and stylish navigation pane is set on the left making getting around the app quick and easy. 

This project is the synthesis of four programming languages: Python, SQL, HTML, and CSS, developed using the Flask web application framework. The Python code is largely structured based on the Model-View-Controller design pattern, with its individual functions performing one or more roles within that structure. For example, the home() function acts primarily as a view. It calls a controller function, init_db(), which retrieves posts from the database (the model), and the view then displays them to the user. 

A SQLite relational database handles data storage with a 'user' table for storing usernames and passwords and a 'post' table for storing posts (author, content, date). The app performs a number of authentication and error checks by querying the database and comparing stored user and post data against Flask session information. 

For the pages themselves, a base HTML template was used that could be extended to cover multiple pages. This approach simplified the code and helped create an appealing consistency across the application. CSS gives style to the structural HTML content by applying properties and values (such as background colors and fonts) to HTML tags and classes, delivering a polished finished product that users will hopefully enjoy.

Blogger is currently being hosted on PythonAnywhere at http://ccamer0n.pythonanywhere.com
