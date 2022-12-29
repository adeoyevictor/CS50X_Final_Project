# My Blog App
### Video Demo: https://youtu.be/cAVT0g4uY0s
### Description:
A Blog app created using python, flask, sql, html and bootstrap
Functionalities include Register, Login, Create post, View post content, Edit post content, Delete post, Logout

### Database Design:

The database contains two tables, posts and users joined by the user id. The posts table contains the id of the post, id of the user that created the post, date created, the title and post content. The users table contains the auto generated user id, username, password hash. 


### Register: 
To register provide a unique username, password and confirm password. If successful you're automatically logged into the app and your user id is added to the session

### Login:
Provide your username and password. If successful you'll be redirected to the home page with all the blog posts

### Create post:
To add a new post click on New Post on the Navbar and provide a post title and content. If successfull you'll  be redirected to the homepage with the newly created post displayed

### View post content:
Click on any post title on the home page to view the post content

### Edit post content:
Click edit on any post on the home page. You'll be routed to an edit page to provide the new contents. If successful you'll be redirected to the homepage which shows recent edit made.

### Delete post
Click edit on any post on the home page. You'll be routed to an edit page. Click on the Delete post button to delete the current post. If successful you'll be redirected to the homepage which shows recent edit made.

### Logout
Click logout to clear the saved data in the session. If successful you'll be routed to the login page