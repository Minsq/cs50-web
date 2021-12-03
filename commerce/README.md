## Commerce 
Design an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

- [project link](https://cs50.harvard.edu/web/2020/projects/2/commerce)
- [project screencast](https://youtu.be/sFyOeFenp1Q)

<video src='https://youtu.be/sFyOeFenp1Q' width=180/>

## Background
In the distribution code is a Django project called commerce that contains a single app called auctions.

First, open up auctions/urls.py, where the URL configuration for this app is defined. Notice that we’ve already written a few URLs for you, including a default index route, a /login route, a /logout route, and a /register route.

Take a look at auctions/views.py to see the views that are associated with each of these routes. The index view for now returns a mostly-empty index.html template. The login_view view renders a login form when a user tries to GET the page. When a user submits the form using the POST request method, the user is authenticated, logged in, and redirected to the index page. The logout_view view logs the user out and redirects them to the index page. Finally, the register route displays a registration form to the user, and creates a new user when the form is submitted. All of this is done for you in the distribution code, so you should be able to run the application now to create some users.

Run python manage.py runserver to start up the Django web server, and visit the website in your browser. Click “Register” and register for an account. You should see that you are now “Signed in as” your user account, and the links at the top of the page have changed. How did the HTML change? Take a look at auctions/templates/auctions/layout.html for the HTML layout of this application. Notice that several parts of the template are wrapped in a check for if user.is_authenticated, so that different content can be rendered depending on whether the user is signed in or not. You’re welcome to change this file if you’d like to add or modify anything in the layout!

Finally, take a look at auctions/models.py. This is where you will define any models for your web application, where each model represents some type of data you want to store in your database. We’ve started you with a User model that represents each user of the application. Because it inherits from AbstractUser, it will already have fields for a username, email, password, etc., but you’re welcome to add new fields to the User class if there is additional information about a user that you wish to represent. You will also need to add additional models to this file to represent details about auction listings, bids, comments, and auction categories. Remember that each time you change anything in auctions/models.py, you’ll need to first run python manage.py makemigrations and then python manage.py migrate to migrate those changes to your database.