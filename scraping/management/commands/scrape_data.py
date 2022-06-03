from django.core.management.base import BaseCommand
from models import Product
from scraper import *

class Command(BaseCommand):
    help = 'import squirrel data from csv file'

    def handle(self, link, **options):
        data = detail(get_all_pro_urls(link))
        for i in range(len(data)):
            _, created = Product.objects.get_or_create(
                name = data.iloc[i]['productName'],
                discription= data.iloc[i]['productDescription'],
                price = data.iloc[i]['productPrice'],
                color = data.iloc[i]['productColor'],
                size = data.iloc[i]['productSizes'],
                category = data.iloc[i]['productCategory'],
                image = data.iloc[i]['imageLinks'],
                url = data.iloc[i]['productUrl'],
            )

