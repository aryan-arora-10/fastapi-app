# THE README.MD FASTAPI 
####    FastAPI,Docker, PostgreSQL,ORM,CI/CD freecodecamp sanjeev thiagarajan

## pointers and venv setup    
```
1. The venv folder is the virtual environment named venv. It's localized to this folder directory
change interpreter path in vscode Command palette then use virtual env in the terminal as well
2. "python3 -m venv venv" to create a virtual env in terminal
3. "source venv/bin/activate" to activate in the terminal using the file in bin/ in venv/
4.  we put main.py in app folder amd make an empty __init__.py file to let pyhton know that this is a package
5. "pip install psycopg2-binary" cuz just install 'psycopg2' didn't work
6.  Python version 3.10.12
7.  sudo apt install python3.10-venv 
```

## Different versions of main.py oldmains/
```
1. oldmains/ folder files 'main1,main2,main3' contain the api which modifies data stored in a local dictionary to simulate the operations.
2. 'main4.py' establishes connection with the PostgreSQL RDS and we write pure SQL to perform CRUD operations on out dat
```

## Ensure you delete all env secrets
```
make sure to Ctrl+F for test-mum-db,db_user,password,secret key etc. Make sure to remove it befor checking into any version control.
Secrets would mostly be in the oauth2.py and database.py files. ALSOO CHECK THE OLDMAINS FOLDER for files which will contain rds url 
password in the try blocks
```
## when creating foreign keys
### standard syntax for foreign keys
```
votes_user_id_fkey this is for the user_id cloumn in votes table
columns (user_id -> id)
this references id column from users table and creates a column user_id in the votes table
```

## ALEMBIC 
### models.base from database.py ansd shemas.py
```
once alembic i ssetup to track the state of th edb using revisons. We 
no longer need **models.Base.metadata.create_all(bind=engine)** in main.py
```
### To prevent issues with Alembic migrations:
```
> Plan Dependencies: Define your tables and their relationships clearly before creating migrations to avoid dependency conflicts.

> Sequential Migrations: Ensure migrations that add foreign keys are always sequenced after the creation of the referenced tables.

> Test Migrations: Apply migrations in a testing environment first to catch and resolve issues before they reach production.Use 

> Labels: When working with branches, use labels to identify and manage them properly.

> Alembic Heads: Regularly check the alembic heads to ensure there is only one head unless multiple heads are intentional due to branching.

> Revisions Order: Be careful with the order of down_revision in your script, which should reflect the correct dependency order.

> Migrate Step by Step: Apply migrations incrementally rather than jumping to the head when there are multiple changes, to ensure each step is successful.
```
### ALEMBIC GENERAL COMMANDS
```
alembic current 
alembic heads
alembic history
```
### CORS
```
>   fetch("http://localhost:8000").then(res => res.json()).then(console.log)
Perform a get request from the console of the a website. If you navigate to google
or YT and run this you get a CORS error because the requests thare being made to fromYT are not going to the youtube domain but a separate domain from yt and thus requests from that origin (YT over here) don't go through
```