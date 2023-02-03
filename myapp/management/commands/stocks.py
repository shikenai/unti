from django.core.management.base import BaseCommand
import pandas as pd
from unti.settings import BASE_DIR
from myapp.models import Brand, Trades
import time


def reg_brands_from_csv():
    df = pd.read_csv(BASE_DIR / "data/brand.csv")
    de_records = df.to_dict(orient='records')
    model_inserts = []
    for d in de_records:
        model_inserts.append(Brand(
            nation=d["nation"],
            market=d["market"],
            brand_name=d["brand_name"],
            code=d["code"],
            division=d["division"],
            industry_code_1=d["industry_code_1"],
            industry_division_1=d["industry_division_1"],
            industry_code_2=d["industry_code_2"],
            industry_division_2=d["industry_division_2"],
            scale_code=d["scale_code"],
            scale_division=d["scale_division"]
        ))
    Brand.objects.bulk_create(model_inserts)


def reg_trades_from_csv():
    df = pd.read_csv(BASE_DIR / "data/trade.csv")
    de_records = df.to_dict(orient='records')
    model_inserts = []
    t1 = time.time()
    # {'Unnamed: 0': 2276171, 'id': 2276173, 'brand': 'ニチレイ(東証１部:2871)', 'brand_code': '2871.jp',
    #  'trade_date': '1999-04-06', 'open_value': 491.157, 'close_value': 489.357, 'high_value': 496.586,
    #  'low_value': 480.317, 'volume': 312293}
    for d in de_records:
        model_inserts.append(Trades(
            brand=Brand.objects.get(code=d["brand_code"].split(".")[0], nation=d["brand_code"].split(".")[1]),
            brand_code=d["brand_code"],
            trade_date=d["trade_date"],
            open_value=d["open_value"],
            close_value=d["close_value"],
            high_value=d["high_value"],
            low_value=d["low_value"],
            volume=d["volume"]
        ))
    print(time.time()-t1)
    Trades.objects.bulk_create(model_inserts)


class Command(BaseCommand):
    help = "register TSE brands"

    def add_arguments(self, parser):
        parser.add_argument("first", type=str)

    def handle(self, *args, **options):
        if options["first"] == "aaa":
            reg_brands_from_csv()
        elif options["first"] == "bbb":
            reg_trades_from_csv()
