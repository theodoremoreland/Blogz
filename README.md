# Blogz

A Python (Flask) web application where multiple users can create their own Blog (updated to use Flask blueprints and Bootstrap CSS). See below for a preview of the application.

_This was originally a homework assignment for LaunchCode's Lc101 (2018)_

<img src="presentation/thumbnail.png" width="700">

## Technologies Used

- Python
- Flask
- Flask_sqlalchemy
- PostgreSQL
- HTML/CSS
- Bootstrap

# How to run locally

Whether you are running the app directly on a Windows OS or indirectly via Docker, there are a few things you need to do in order to setup the application:

- You need your own PostgreSQL database instance.
- You need to create a folder named `instance` in the `application` folder. Then create a file called `config.cfg` in `application/instance/` mimicking the template provided in `application/instance_example/config.cfg.example` wherein the empty strings are replaced with values relating to your instance's secret key and PostgreSQL URI.
- If you are trying to run this application directly on a Windows OS, you will need to install `Python 3.11`.
- Otherwise, you will need to install Docker so you can run the application through Docker.

## Run on Windows

Assumes you are using a modern Windows client OS such as Windows 11 or Windows 10 and that Python 3.11 is installed.

**It is assumed the user is at the root of this project and is using a UNIX style command line environment when referencing the CLI commands below.**

Open terminal at root of this project then move into application/ directory:

```
cd application/
```

Create venv folder in application folder using Python 3.11:

```
python3.11 -m venv venv
```

Activate venv:

```
source venv/Scripts/activate
```

Install python packages to venv:

```
pip install -r requirements.txt
```

Start application:

```
python application.py
```

## Run on Docker

Firstly, confirm that Docker is installed and running. Next confirm that no other application is using port `5000` as port `5000` is needed for the Flask server. If you need to run Flask on an alternative port, you can modify the last line in the `application/application.py` file.

**It is assumed the user is at the root of this project and is using a UNIX style command line environment when referencing the CLI commands below.**

Open terminal at root of this project then move into docker/ directory:

```
cd docker/
```

Build Docker image and start Docker container:

```
docker compose up --build
```

Visit: http://localhost:5000 to use the application.

# Home / Bloggers Page (Before Sign up)

<img src="presentation/1.PNG" width="900">

# Log In Page

<img src="presentation/2.PNG" width="900">

# Sign Up Page (making account for Carl Jung)

<img src="presentation/3.PNG" width="900">

# Account for Carl Jung has been created

<img src="presentation/4.PNG" width="900">

# Home / Bloggers Page (After multiple sign ups)

<img src="presentation/5.PNG" width="900">

# Publishing a blog post (as Carl Jung)

<img src="presentation/6.PNG" width="900">

# After publishing post

<img src="presentation/7.PNG" width="900">

# View of Carl Jung's Blog after first post

<img src="presentation/8.PNG" width="900">

# View of Carl Jung's Blog after multiple posts

<img src="presentation/9.PNG" width="900">

# All Posts - Animated - (multiple users)

<img src="presentation/1.gif" width="900">

# View #1 All Post (multiple users)

<img src="presentation/10.PNG" width="900">

# View #2

<img src="presentation/11.PNG" width="900">

# View #3

<img src="presentation/12.PNG" width="900">

# Favorite Posts

<img src="presentation/16.PNG" width="900">
<img src="presentation/17.PNG" width="900">
<img src="presentation/18.PNG" width="900">
<img src="presentation/13.PNG" width="900">
<img src="presentation/15.PNG" width="900">
<img src="presentation/14.PNG" width="900">
