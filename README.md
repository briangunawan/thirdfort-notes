

# thirdfort-notes
Notes API for Thirdfort application

## How to run the application:
1. Install dependencies by running `pip install -e.`
2. Set FLASK_APP environment variable.
	* Windows:
		`set FLASK_APP = flaskr`
	*  Linux/Mac:
		`export FLASK_APP=flaskr`
3. Run the app as a local server
	`flask run`

### Testing
To run test cases for each endpoint, run `pytest` in root directory. 

## How to use the API
### Notes 
Requests require a user to be logged in. 
| Endpoint | Description |
|--|--|
| /notes | Methods: **GET**, **POST** <br><br> GET: Returns list of *note* objects that is owned by current logged in user.<br><br> POST: Create a new note belonging to logged in user. Requires 2 arguments in request `title: String` and `body: String`. Returns note's ID|
|/notes/archived| Methods: **GET** <br><br> GET: Get list of archived note objects owned by current user. Returns a list of *note* objects.|
|/notes/\<noteid\>|Methods: **GET**, **DELETE**, **PUT** <br><br> GET:  Returns *note* object with ID: \<noteid\>. <br><br> DELETE: Delete *note* with ID: \<noteid\> <br><br> PUT: Updates *note* with ID: \<noteid\> with arguments. Requires `title: String`, `body: String` and `archived: Boolean`|

### Note Object
|Variable| Description|
|---|--|
|noteid| String generated when creating a new Note object. |
|title|String holding the title of the Note|
|body|String holding the body of the Note|
|archive| Boolean denoting whether the note is archived or not. True if archived. False otherwise. Default: False|

### Authentication
|Endpoint| Description|
|--|--|
|/login|Methods: **POST** <br><br> POST: Set user of current session. Requires `username`.|
|/logout| Methods: **GET** <br><br> GET: Logs user out of current session.|

## Architecture
For the web app, I decided to use the python web framework **Flask** as it is a language I am very comfortable with and have some experience using Flask before. It is more lightweight and implements a simpler file system than python framework alternatives like Django while keeping core functionality.

For the database, I decided to use a neo4j's implementation of a graph database. They also offer free trial hosting which is where the database currently sits. I decided to use this as an oppurtunity to learn a new database type that I have not much experience with. I decided on a graph database as it has the advantage of a less structured data type construction while keeping the important relationship data. The graph database is quite simple consisting of 2 node types, `User` and `Note` and 1 edge type denoting the relationship  where a `Note->BelongsTo->User`. The main alternative I considered is a mysql database as it is one I have a lot of experience in however having strict typing forces the note to only consist of a single type without modification.

## Extenstions and Improvements
### Authentication
I would add a password field for greater security which would require hashing and salting before storing in the database. I would also add a dedicated register user endpoint and update user endpoint which creates and edits the User node respectively.

### Notes
I would add a feature to allow you to add multiple owners of a note to allow access to multple users. This would only require an endpoint to add more BelongsTo relation from the Note to a User.

Extending from that I could implement a third node type denoting a Group of Users and Notes can belong to a Group which results in ownership for all Users in that Group. Example: Business group or Developer group.