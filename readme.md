# Social Media CRUD API Using FastAPI 🖥️

Welcome to the Social Media CRUD API documentation. This project is a backend service built with FastAPI in Python, designed to handle basic social media operations such as creating, reading, updating, and deleting posts. Users can also upvote and downvote posts. The API uses OAuth2 with JWT tokens for authentication, ensuring secure access to the application. This covers the routes and installation. 
#### Detailed project info is available in 
### : [variousmarkdowns/readmeforme.md](./variousmarkdowns/readmeforme.md)

## FEATURES 📜

- **CRUD Operations**: Create, read, update, and delete posts.
- **Vote System**: Users can upvote or downvote posts.
- **Authentication**: Secure login system using OAuth2 with JWT tokens.
- **Database**: PostgreSQL hosted on AWS RDS.
- **ORM**: SQL Alchemy for database interactions and Alembic for database migrations.
- **Hosting**: Application hosted on AWS EC2.
- **Reverse Proxy**: Nginx used to direct requests from the internet to the application.
- **CI/CD**: Automated testing and deployment using GitHub Actions, Docker Compose, and pytest.

## API ENDPOINT 🗂️

### Access the API at: [api.aryandev.org](http://api.aryandev.org)

## ROUTES OF THE API
### See the OPENAPI documentation and interact with routes
### Openapi documentation:       [api.aryandev.org/docs](https://api.aryandev.org/docs)

```
    Use the authorize section to login to your user after creating one and 
    access the protected paths with the lock icon 🔒 on them 
```
### This API  has 4 routes

### 1) Auth route ✅

#### This route is about login system. Create a user and then login.

### 2) Post route 📝

#### This route is reponsible for creating post, deleting post, updating post and fetching post

### 3) Users route 🧑🆔

#### This route is about creating users and searching user by id


### 4) Vote route  ⬆️⬇️

#### This route is about likes or vote system and this route allows us to upvote or downvote using 'dir' param


## GETTING STARTED
### Prerequisites

- Python 3.10
- Docker & Docker Compose
- An AWS account (for RDS and EC2)

### Local Installation

1. Clone the repository:
```
git clone https://github.com/aryan-arora-10/fastapi-app.git
```
2. Navigate to the project directory:
```
cd fastapi-app
```
3. Create venv
```
see variousmarkdowns folder for detailed instructions including the systemd service
```

4. Install dependencies
```
pip install -r requirements.txt
```
5. Setup env vars in .env
```
Your env vars will allow you to run this app locally.
    DATABASE_HOST: str  could be a local postgres container or a hosted DB
    DATABASE_PORT: str
    DATABASE_PASSWORD:str 
    DATABASE_NAME:str
    DATABASE_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_NAME_TEST:str

This will enable one to run their own version of the app and see it on localhost:8000
```

6. Start app using docker compose
```
docker compose -f dev-docker-compose.yaml up -d

>   -d flag runs in detached mode

>   --build flag might be required to detect changes in build context
```