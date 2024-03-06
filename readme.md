# Social Media CRUD API Using FastAPI

Welcome to the Social Media CRUD API documentation. This project is a backend service built with FastAPI in Python, designed to handle basic social media operations such as creating, reading, updating, and deleting posts. Users can also upvote and downvote posts. The API uses OAuth2 with JWT tokens for authentication, ensuring secure access to the application.

## Features

- **CRUD Operations**: Create, read, update, and delete posts.
- **Vote System**: Users can upvote or downvote posts.
- **Authentication**: Secure login system using OAuth2 with JWT tokens.
- **Database**: PostgreSQL hosted on AWS RDS.
- **ORM**: SQL Alchemy for database interactions and Alembic for database migrations.
- **Hosting**: Application hosted on AWS EC2.
- **Reverse Proxy**: Nginx used to direct requests from the internet to the application.
- **CI/CD**: Automated testing and deployment using GitHub Actions, Docker Compose, and pytest.

## API Endpoint

Access the API at: [api.example.com](http://api.example.com)

## ROUTES OF THE API
### See the OPENAPI documentation and interact with routes
:       [api.aryandev.org/docs](https://api.aryandev.org/docs)
#### This API  has 4 routes

### 1) Auth route

#### This route is about login system. Create a user and then login

### 2) Post route

#### This route is reponsible for creating post, deleting post, updating post and Checkinh post

### 3) Users route

#### This route is about creating users and searching user by id


### 4) Vote route

#### This route is about likes or vote system and this route contain code for upvote or back vote there is not logic about down vote


## Getting Started
### Prerequisites

- Python 3.10
- Docker & Docker Compose
- An AWS account (for RDS and EC2)

### Installation

1. Clone the repository:
```
git clone https://github.com/aryan-arora-10/fastapi-app.git
```
2. Navigate to the project directory:
```
cd fastapi-app
```
3. Create venv

4. Install dependencies
```
pip install -r requirements.txt
```
5. Setup env vars in .env

6. Start app using docker compose
```
docker compose -f filename.yaml up -d

-d flag runs in detached mode
```