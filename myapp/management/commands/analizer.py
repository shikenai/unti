from django.core.management.base import BaseCommand
import pandas as pd
from unti.settings import BASE_DIR
from myapp.models import Brand, Trades
import time
from django_pandas.io import read_frame


def test():
    _trades = Trades.objects.filter(brand_code="7203.jp").order_by("trade_date")
    n = _trades.count()
    x = 100
    if n < x:
        n_minus = 0
    else:
        n_minus = n - x
    df = read_frame(_trades.all()[n_minus:n])
    print(df)


class Command(BaseCommand):
    help = "register TSE brands"

    def add_arguments(self, parser):
        parser.add_argument("first", type=str)

    def handle(self, *args, **options):
        test()
