# Flask Assignment
In this Flask assignment, a robust user management system has been created using Python and Flask. It includes routes for user registration, sign-in, password reset, and both updating and deleting user accounts. The application uses JWTs for secure authentication and password hashing for protecting user credentials. Environmental variables are utilized for sensitive database configuration to ensure security and flexibility. This setup allows for efficient user management and secure access control in a web application.

### Technology Stack

As the name suggests, this repository is built on top of Python,Flask & PostgreSQL, however, in the implementation detail, we will find other supporting technologies as well.

<img src="https://img.shields.io/badge/PostgreSQL-%2331575F?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" width="60" height="20"/>: For the database to store user information, complaints, and other relevant data.

<img src="https://img.shields.io/badge/Python-%233776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" width="60" height="20"/>: The programming language used to build the application.

<img src="https://img.shields.io/badge/Flask-%23000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" width="60" height="20"/>: The web framework used to build the backend of the application.

<img src="https://img.shields.io/badge/Postman-%23FF6C37?style=for-the-badge&logo=postman&logoColor=white" alt="Postman" width="60" height="20"/>: For testing API endpoints and ensuring smooth communication between frontend and backend.





### Running the Project
Before running the application, make sure you have installed python in your machine.

1. Clone the project
    ```bash
    git clone https://github.com/Md-Roni024/Flask_Assignment
    ```  

2. Go to the project directory and install dependencies
    ```
    cd Flask_Assignment
    pip install -r requirements.txt
    ```
3. Create a .env file then add your variables credentials as like:
    ```
    USER = "Postgress User Name"
    HOST = "Host Name"
    DATABASE = "Database Name"
    PASSWORD = "Postgress Password"

    //Server Listening PORT
    PORT = ""
    ```
4. Start the project
    ```
    python app.py
    ```
    After successfully run the project it will launch in port 5000. and Root URL will be : http://127.0.0.1:5000


### REST API
For managing user information I build 5 endpoints.They are responsible for register,signin,reset-password,update user and delete user. 

- <h3>Create a new USER</h2>
  Method: POST

  URL: http://127.0.0.1:5000/register

  Input looks like:
  
  ```json
  {
    "username": "demo",
    "password": "demo",
    "first_name": "Roni",
    "last_name": "Hossain",
    "email": "demo@example.com",
    "role": "Admin",
    "active": true
  }

  ```

- <h3>USER siginin</h2>
  Method: POST

  header: Authorization Token

  URL: http://127.0.0.1:5000/register/signin/

  Signin input looks like:

  ```json
   {
    "username": "user_01",
    "password": "user24"
   }
  ```

- <h3>Reset password</h2>
  Method: PUT

  URL: http://127.0.0.1:5000/register/reset-password
  
  header: Authorization Token

  Input Look likes:
  ```json
  {
    "username": "demo2",
    "new_password": "demo2"
  }
  ```


### Design Database Schema
- Database Name: <span style="color:red;font-size:15px;font-weight:bold">hotel_db</span>

- Hotel Deatils Table
  ```sql
  CREATE TABLE hotel_details(
      id SERIAL PRIMARY KEY,
      username VARCHAR(255) UNIQUE NOT NULL,
      first_name VARCHAR(255) NOT NULL,
      password_hash VARCHAR(255) NOT NULL,
      email VARCHAR(255) NOT NULL,
      role TEXT,
      created_at Date,
      updated_at Date,
      active boolean
  );

  ```

### Future Improvements




### Contributing
- Contributing is an open invitation for collaboration on the project. You're encouraged to participate by opening issues for bugs or feature requests and submitting pull requests with your improvements or fixes. Your contributions help enhance and grow the project, making it better for everyone.


### Contact

- For any questions or feedback, please reach out to me at roni.cse@gmail.com. I welcome all inquiries and look forward to hearing from you. Your input is valuable and appreciated!

