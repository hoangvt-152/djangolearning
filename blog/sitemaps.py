from .models import Post
from django.contrib.sitemaps import Sitemap
class PostSitemap(Sitemap):
    changefreq = 'weekly'
    piority = '0.9'
    def item(self):
        return Post.published.all()

    def lastmod(self,obj):
        return obj.updated    

