source  ~/django_env/bin/activate
pip3 install Django==4.0.3
django-admin startproject Blog
python3 manage.py startapp blog
Activating the application

sudo apt install python3-psycopg2
pip3 install psycopg2-binary

python3 manage.py makemigrations blog

python manage.py sqlmigrate blog 0001


python3 manage.py migrate

python manage.py createsuperuser

python manage.py runserver

python manage.py shell



>>> from django.contrib.auth.models import User
>>> from blog.models import Post
>>> user = User.objects.get(username='admin')
>>> post = Post(title='Another post',
... slug='another-post',
... body='Post body.',
... author=user)
>>> post.save()



Using exclude()

>>> post = Post.objects.get(id=1)
>>> post.delete()
