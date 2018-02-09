# Capsoul Backend
A python based backend that uses Django to store memories.

## Running the server

To run the server follow the steps below.
You may either follow steps 1 and 2, or instead follow steps 1 and 2 in the docker instructions at the bottom of the page.

Before you start you should have python 2.7 installed. You can download it [here](https://www.python.org/downloads/).

#### 1. Install Django
```
pip install -r requirements.txt
```
#### 2. Get the project running
Add a folder called "db" to your capsoul-backend folder
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

#### 3. Query endpoints
You can check that the server is running by navigating to [localhost:8000](http://localhost:8000). This will show the available routes.

For example [localhost:8000/user/<uname>](http://localhost:8000/users/rabery) would load the following when `uname` is “rabery”.
```
{
    "user_name": "rabery",
    "first": "Ryan",
    "last": "Rabello",
    "phone": "212-479-7990",
    "location": "Walla Walla, WA",
    "photo": "ryan.jpg",
    "email": "ryan.rabello@gmail.com",
    "birthdate": "1992-09-02"
}
```

## Other Notes
#### Running on a different port
You can run the server on a different port by running the following command.
```
python manage.py runserver <port>
```
Where `port` would be the number of the port you want to use.

## Running the Server with Docker
#### Step 1: Install Docker
Mac Download: https://download.docker.com/mac/stable/Docker.dmg

Windows Download: https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe

Linux Instructions:
```
	$ sudo apt-get update

	$ sudo apt-get install \
	 apt-transport-https \
	 ca-certificates \
	 curl \
	 software-properties-common

	$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

	$ sudo add-apt-repository \
	 "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
	 $(lsb_release -cs) \
	 stable"

	$ sudo apt-get update

	$ sudo apt-get install docker-ce
```

#### Step 2: Build and Run the server
Run the `docker-volume-create.sh` and `docker-build.sh` scripts in that order.

The server should now be running on localhost port 42000

#### Step 3: Rebuild server upon changes
To rebuild the server in the Docker container upon changing source files, run the `docker-rebuild.sh` script
