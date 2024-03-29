# THE README.MD FASTAPI 
####    FastAPI,Docker, PostgreSQL,ORM,CI/CD 

## INITIAL POINTERS AND VENV SETUP    
```
1. The venv folder is the virtual environment named venv. It's localized to this folder directory
    change interpreter path in vscode Command palette then use virtual env in the terminal as well
2. "python3 -m venv venv" to create a virtual env in terminal
3. "source venv/bin/activate" to activate in the terminal using the file in bin/ in venv/
4.  we put main.py in app folder amd make an empty __init__.py file to let python know that this is a package
5. "pip install psycopg2-binary" because simply running install 'psycopg2' didn't work.
    Also might need pip httptools and uvlooop before installing gunicorn
6.  Python version 3.10.12 for the most part. Dockerfile use 3.10.13 which is the last patch
7.  sudo apt install python3.10-venv 
```

## DIFFERENT VERSIONS OF MAIN.PY IN oldmains/
```
1. oldmains/ folder files 'main1,main2,main3' contain the api which modifies data stored in a local dictionary to simulate the operations.
2. 'main4.py' establishes connection with the PostgreSQL RDS and we write pure SQL to perform CRUD operations on out dat
```

## CLEANUP ENV VARS AND SECRETS
```
make sure to Ctrl+F for test-mum-db,db_user,password,secret key etc. Make sure to remove it befor checking into any version control.
Secrets would mostly be in the oauth2.py and database.py files. ALSOO CHECK THE OLDMAINS FOLDER for files which will contain rds url 
password in the try blocks
```
## FOREIGN KEYS IN SQL
### standard syntax for foreign keys
```
votes_user_id_fkey this is for the user_id cloumn in votes table
columns (user_id -> id)
this references id column from users table and creates a column user_id in the votes table
```

## ALEMBIC 
### models.base from database.py ansd shemas.py
```
once alembic is setup to track the state of the db using revisons. We 
no longer need   **models.Base.metadata.create_all(bind=engine)**  in main.py.
This maybe still used in pytest when we create a client pytest fixture so that each 
test function gets a new db with all the tables the test is run and then the 
tables are destroyed 
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
### alembic general commands
```
alembic current 
alembic heads
alembic history
```
## CORS
```
>   fetch("http://localhost:8000").then(res => res.json()).then(console.log)
Perform a get request from the console of the a website. If you navigate to google
or YT and run this you get a CORS error because the requests thare being made to fromYT are not going to the youtube domain but a separate domain from yt and thus requests from that origin (YT in this case) don't go through
```

## SET AND UNSET ENV vars
```
export MYNAME=robo  # sets an env variable 
printenv | grep MYNAME 
unset MYNAME
printenv | grep MYNAME          
```
## HAVE ENV vars persist through a reboot
```
Might need to edit bashrc or .profile on the VM itself
```

## PYTEST and it's flags
```
    -s will print our specific codes
    -x will stop the downstream tests when an error occurs in one test
    -v is for increased verbosity
    pytest -s -x testdir/test_functionality.py => run pytest only for that file
```
## SYSTEMD API SERVICE
### symlink of the api.service file
```
The Initial API could run as a systemctl gunifast.service
with it's port set to 8000. A symbolic link (shortcut-esque) was
created in the /etc/systemd/system dir
This symlink points to ~/gunifast.service

When creating the service file we set After = network.target
which forces the service to wait after the network services start
```
### systemctl commands
```
nginx was also installed as a systemctl service
>   to check status
    'sudo systemctl status nginx.service'
>   start and stop
    'sudo systemctl start service'
>   to enable on boot
    'sudo systemctl enable gunifast.service'
>   journalctl can be used to see the logs
```

## CERTBOT AND SSL
```
our LetsEncrypt SSL certificates expire in 90 days. Certbot has a timer which renews the certs as part of
systemctl timers. I had to create this timer as it didn't exist. Check screenshots for the commands and outputs
``` 
## DOCKER
```
When running docker compose --build my be necessary to force a change.
Even though the build context has changed.
```

### DOCKER ON ubuntu 
```
Install docker on the ubuntu vm using
    1. the commands on the docker install on ubuntu page
    2. Uninstall any pre installed/ dangling packages
    3. add the repo to apt -repositories
    4. 'docker run hello-world' to test it
    5. Use below command to prevent docker.sock permission denied
    
    "sudo usermod -aG docker $USER" to add the current user to the group
    
    6. Changing the groups of a user does not change existing logins, terminals, and shells that a user has open. 
    To avoid performing login again, you can simply run: "newgrp docker" 
```