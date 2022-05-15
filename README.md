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

markdown==3.2.1

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

Adding a sitemap to your site
-------
Adding a sitemap to your site

SITE_ID = 1
# Application definition
INSTALLED_APPS = [
# ...
'django.contrib.sites',
'django.contrib.sitemaps',
]


---------
Creating feeds for your blog posts

 feeds.py

class LatestPostsFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog.'
    def items(self):
        return Post.published.all()[:5]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return truncatewords(item.body, 30)


blog/urls.py 
from .feeds import LatestPostsFeed

urlpatterns = [
# ...
path('feed/', LatestPostsFeed(), name='post_feed'),
]

http://127.0.0.1:8000/blog/feed/ 

<p>
<a href="{% url "blog:post_feed" %}">Subscribe to my RSS feed</a>
</p

-----
Adding full-text search to your blog

the contains filter (or its case-insensitive version, icontains)

from blog.models import Post
Post.objects.filter(body__contains='framework')

''Installing PostgreSQL''
sudo apt-get install postgresql postgresql-contrib
pip install psycopg2-binary==2.8.4
su postgres
createuser -dP blog


createdb -E utf8 -U blog blog
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql',
'NAME': 'blog',
'USER': 'blog',
'PASSWORD': '*****',
}

INSTALLED_APPS = [
# ...
'django.contrib.postgres',
]


from django.contrib.postgres.search import SearchVector
from .forms import EmailPostForm, CommentForm, SearchForm
def post_search(request):
form = SearchForm()
query = None
results = []
if 'query' in request.GET:
form = SearchForm(request.GET)
if form.is_valid():
query = form.cleaned_data['query']
results = Post.published.annotate(
search=SearchVector('title', 'body'),
).filter(search=query)
return render(request



path('search/', views.post_search, name='post_search')


Stemming and ranking results
from django.contrib.postgres.search import SearchVector, SearchQuery,SearchRank


search_vector = SearchVector('title', 'body')
search_query = SearchQuery(query)
results = Post.published.annotate(
search=search_vector,
rank=SearchRank(search_vector, search_query)
).filter(search=search_query).order_by('-rank')


http://127.0.0.1:8000/blog/search/



Weighting queries
search_vector = SearchVector('title', weight='A') + \
SearchVector('body', weight='B')
search_query = SearchQuery(query)
results = Post.published.annotate(
rank=SearchRank(search_vector, search_query)
).filter(rank__gte=0.3).order_by('-rank')



Searching with trigram similarity


psql blog
CREATE EXTENSION pg_trgm;
from django.contrib.postgres.search import TrigramSimilarity
results = Post.published.annotate(
similarity=TrigramSimilarity('title', query),
).filter(similarity__gt=0.1).order_by('-similarity')