# Backend blog test tasks

* First clone from reposotory to your local folder using command
    - `git clone git@github.com:Alymbekov/backend_blog_test_tasks.git .`

* create virtual environment using command

    - `python3 -m venv <name of your environment>`

* activate your virtual environment
    
    - `source <name of your environment>/bin/activate`
    
* install requirements by commond

    - `pip3 install -r requirements.txt`
    
* create on near manage.py file .env, same as .env_example

    - generate secret key to put in to .env file
    
* make migrations
    - `python manage.py makemigrations`
    - `python manage.py migrate`

* create superuser
    - `python manage.py createsuperuser`
    
* finally you can run your project

    - `python manage.py runserver`

* Also you can run in other terminal
    - `celery -A main  worker --loglevel=info`
    
* Also you can run in other terminal
    - `redis-server`

#Running a project with docker

    -  `docker-compose up --build`

