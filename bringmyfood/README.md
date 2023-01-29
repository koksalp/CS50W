# BRINGMYFOOD  
This is the final project that I have made for CS50's Web Programming with Python and Javascript.  

See the project in action [here](https://www.youtube.com/watch?v=upDkRRhVe5E)  
## What it is about 

Since the most famous apps from leading tech companies have been recreated on each problem set throughout the course, a popular service from a sector that has increased its importance for the last decade and includes many successful apps worldwide has been chosen as a subject of the final project and that is why a food delivery app has been implemented. Users can login as either customer or restaurant owner. Users that do not own a restaurant (customers) can select a restaurant listed in the homepage and order any product that the restaurant offers. Restaurant owners, on the other hand, can also do anything that a customer can do because they are also customers. Other than that, they are allowed to open restaurants and they can manage them all they want. 

## FILES & DIRECTORIES 
* `main directory`     
    * `bringmyfood` 
        * `models.py` 
            * `User class`  
                * This is the default User model that has been extended after two more fields have been added which are fields to store user's phone number and whether the user is a restaurant owner or not.  
            * `Customer class`  
                * This model only has two fields. One field is for referencing another model which is the User model, and the other one is for customer balance which indicates how much money customers currently have in their customer accounts. 
            * `Owner class`  
                * This model seems to have only one field which references to the User field but it also has one to many relationship with Restaurant model since one owner can own multiple restaurants. One restaurant might also have multiple owners but for simplicity, that is not the case. The only purpose of this model is to keep track of relationships between owners and their restaurants.  
            * `Restaurant class` 
                * This model has been created to keep track of restaurant informations such as restaurant name, address, category (what kind of food/beverage they provide) and phone number. It also has one to many relationship with owner model. This way, restaurant owners can be accessed as well as all the restaurants an owner has.    
            * `Product class` 
                * This model is used to store information about any kind of product that a restaurant offers. The model has multiple fields to store all necessary information about a food/beverage such as name, price and calories. It also has one to many relationship with Restaurant model so that each restaurant can have unique products that only belongs to them. 
            * `Order class` 
                * This is the most complicated model of all. It has multiple foreign keys html referencing customer and restaurant models because each order has a customer waiting for delivery as well as a restaurant that delivers the order. It has a DateTimeField to keep track of the time when customer orders. The model has many to many relationship with Product model because an order can consist of multiple products and one product can be in multiple orders. There are 3 more fields. One of them indicates whether the order is still active (true by default until it gets cancelled or delivered). Another one indicates whether a restaurant has deleted an order or not. The last field indicates the total amount of order that customer needs to pay. 
            * `Amount class`  
                * This model is used as a way of keeping track of the amount of each product ordered. There must be more efficient ways to achieve this goal but I honestly could not come up with anything better than this approach.  
        * `views.py` 
            * `index function` 
                * Responsible for rendering the homepage. All the restaurants are listed in the homepage in alphabetical order. Users can also sort the restaurants by one of the following options: all, open and close. 
            * `login_view function`  
                * Responsible for logging users in. 
            * `logout_view function` 
                * Responsible for logging users out. 
            * `register function` 
                * Responsible for registering users. 
            * `orders function` 
                * Responsible for rendering a page that lists all the orders that a customer has created. Customers can see details of each order they have made such as restaurant info, when the order has been created, whether or not the order is still active as well as the products they have ordered and their amounts. Furthermore, customers can cancel their ordes here. 
            * `profile function` 
                * Renders profile page that has information about the user. Furthermore, users can add money to their accounts. For simplicity, neither credit card validation has been added nor credit card informations is asked to customers. This is a feature that can easily be added later on. 
            * `owner_manage function` 
                * Responsible for rendering a page to restaurants ownersonly. They can see all their restaurants here as well as they can open a brand new restaurant. 
            * `restaurant function` 
                * This is the most complicated function so far and is responsible for multiple operations. If customers access this page by GET request, they see restaurant information as well as menu. They can take a look at all the products and create an order after selecting amount of each product. They can successfully order if they can afford it, otherwise they get a message indicating that the order is unsuccessful. If owner of that restaurant visits this page, they see the products only since they can not order. Besides, they can add products to the menu or they can check all the orders. Restaurant owners can delete orders, but they should press the ready button first to indicate that the order is delivered to customer. The scenerio where a restaurant owner cancels an order due to several reasons is not handled in this app but it can be easily added as a feature. Furthermore, a PUT request is sent to this route when a customer cancels and order or a restaurant owner deletes an order after he/she clicks the button indicating that the order is ready. 
            * `product function` 
                * Responsible for rendering a page that shows information about a specific product. 
            * `order function` 
                * This is an API route and it only accepts POST requests. When a customer creates an order in the page that is rendered by orders function, a POST request gets sent to this route and if customer's balance is high enough to afford the price, an order is created successfuly, otherwise an error message is returned.  
        * `helpers.py` 
            * This file has been created to keep functions that are not direclty related to rendering HTML pages seperated from views.py file. It only contains one function but the number of functions in this file should increase as more features are added to the app. That single function is called proper_string and it is used to put user input into a certain format. For instance, it is called when a new restaurant is opened. Restaurant name, category and address info is stored in database after they follow a certain format.   
        * `static/bringmyfood` 
            * `add_money.js`  
                * Responsible for hiding and showing add money button in profile page. When users add money to their accounts, the page gets re-rendered and a message gets displayed indicating the operation is successful. The message also gets dissappear after a certain amount of time thanks to this js file. 
            * `layout.js` 
                * Keeps track of the active link in the navbar and helps users notice what page they are currently in. 
            * `orders.js`  
                * Sends a PUT request to 'restaurants' route so that customers can cancel their orders. 
            * `owner_manage.js`  
                * Does nothing but hiding and showing buttons in the page where owners can manage their restaurants. 
            * `restaurant.js`  
                * Responsible for customers to create orders and restaurant ownersto delete orders after indicating that the order is ready. These are the major operations of this app and they are done in client side which means that the pages does not need to be reloaded. Thus, it is the most important js file in the app. 
            * `styles.css` 
                * All the styling is managed in this file. There is no other css file for this app. 
        * `templates/bringmyfood`  
            * `index.html`  
                * Homepage of the app. All restaurants are displayed here. 
            * `layout.html` 
                * General structure of pages. It includes the common structure that all pages share together such as navbar and the links inside of it.  
            * `login.html` 
                * Login page, users can login here.  
            * `register.html`   
                * Register page, users can register in this page. 
            * `orders.html` 
                * All the orders that belong to users are displayed here. 
            * `owner_manage.html` 
                * Restaurant owners can manage their restaurants here. Restaurant owners can see all their restaurants here and they can open a new one. 
            * `product.html`  
                * This page shows a specific product as well as information about it. 
            * `profile.html` 
                * This page shows a specific user as well as information about them. Users can also add money to their customer accounts if they visit their own page. 
            * `restaurant.html` 
                * This page displays a specific restaurant and all the information about it can also be seen here as well as the menu. Customers can order in this page. If a restaurant owner visits the page of his/her restaurant, he/she can add new products to menu or see all the orders. They can also press ready button to indicate that the order is delivered. They can then delete that order if they no longer want to see it. 
## Distinctiveness and Complexity 

The project is distinct from all the previous projects in problem sets in terms of project idea and functionality. It is neither an e-commerce app nor a social media app. 

The project is more complex than the previous projects because there are numerous models having complicated relationships with each other. For instance, none of the previous projects in problem sets I have done before includes ManyToManyField but this project does. All tables are connected to at least one other table, furthermore, there are some tables having relationships with multiple tables. Other than models being more complex, ajax functionality has been used many times meaning that sending HTTP requests to our own server makes it faster since there is no need to reload a page, thus, this also adds more complexity to the project considering multiple pages have that ability. 

## How to run this application 
* Install project dependencies by running `pip install -r requirements.txt `
* Make and apply migrations by running `python manage.py makemigrations` and `python manage.py migrate` in the main directory where `manage.py` is. 
* You can then run `python manage.py runserver` to start a web server on your local machine and visit the URL that appears (most probably `localhost:8000`) 