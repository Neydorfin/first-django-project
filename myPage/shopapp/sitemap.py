from django.contrib.sitemaps import Sitemap
from shopapp.models import Product



class ShopSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    
    def items(self):
        return Product.objects.select_related("created_by").prefetch_related("images").filter(archived=False)

    def lastmod(self, obj: Product):
        return obj.created_at

        