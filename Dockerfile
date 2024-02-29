FROM python:3.10.12

#set the working directory so that we only need to use relative paths
WORKDIR /usr/src/app

# we copy requirements and pip install before copying the code
# so that these steps are cached as layers as as they don't change that frequently
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

#copy everything in current dir to workdir inside the image
COPY . .

#command to the run the app S
CMD [ "uvicorn","app.main:app","--host","0.0.0.0","--port","8000" ]
