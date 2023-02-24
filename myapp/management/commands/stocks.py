from django.core.management.base import BaseCommand
import pandas as pd
from unti.settings import BASE_DIR
from myapp.models import Brand, Trades
import time
import pandas_datareader.data as data
import datetime as dt
import os
from django_pandas.io import read_frame


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
    print(time.time() - t1)
    Trades.objects.bulk_create(model_inserts)


def get_trades_from_stooq():
    print('from stppq')
    # これはこれでいい感じだけど、一旦処理の順番を考えて見ることにした
    # t1 = time.time()
    # df = read_frame(Trades.objects.all().order_by("trade_date"))
    # df = df[["trade_date", "brand_code"]].groupby("brand_code").max()
    # df = df.reset_index()
    # list_brand_code = df["brand_code"].to_list()
    # list_trade_date= df["trade_date"].to_list()
    # _df = df["trade_date"].sort_values().drop_duplicates().to_list()
    # dict_tradedate_brandcode = {}
    # print(time.time() - t1)


    # get_target_brands("jp")[0] は、既にある程度の取引状況をデータとして保有しているもの
    # →各銘柄ごとの、取引最終日を取得し、その日以降のデータを取得する必要がある

    # →全ての銘柄について、一律指定した日からデータ取得日までのデータを取得すれば良い
    # print("8888.jp" in get_target_brands("jp")[0])


def sort_out_2lists(list1, list2):
    # ベン図の交わる部分
    intersection = set(list1) & set(list2)
    # ベン図のうち、どちらかに含まれる部分
    union_minus_intersection = set(list1) ^ set(list2)
    # ベン図のうち、list1にのみ含まれる部分
    only_list1 = set(list1) & set(union_minus_intersection)
    # ベン図のうち、list2にのみ含まれる部分
    only_list2 = set(list2) & set(union_minus_intersection)
    return intersection, only_list1, only_list2


def get_target_brands(nation):
    # 最新の銘柄リスト
    list_csv_brand = list(pd.read_csv(BASE_DIR / "data/before_brand.csv")["コード"])  # ここでは数値として取得しているみたい
    list_csv_brand_str = [str(c) + "." + nation for c in list_csv_brand]  # だから文字列に変換する
    # tradesに登録済の銘柄リスト
    brands_in_trades = list(Trades.objects.all().order_by("brand_code").distinct().values_list('brand_code', flat=True))

    return sort_out_2lists(list_csv_brand_str, brands_in_trades)[0], \
        sort_out_2lists(list_csv_brand_str, brands_in_trades)[1], sort_out_2lists(list_csv_brand_str, brands_in_trades)[
        2]


def get_tse_brands():
    # 東証から銘柄データを取得し、before_brand.csvとして全体を格納。この際、登録されていない銘柄は一括登録する。
    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    new_brand = pd.read_excel(url)
    old_brand = pd.read_csv(os.path.join(BASE_DIR, "data", "before_brand.csv"))

    added_brand = new_brand[~new_brand["コード"].isin(old_brand["コード"])]

    added_brand_records = added_brand.to_dict(orient="records")
    brand_model_inserts = []
    for d in added_brand_records:
        _brands = Brand.objects.filter(code=d["コード"])
        if _brands.count() == 0:
            brand_model_inserts.append(Brand(
                nation="jp",
                market="東証１部",
                brand_name=d["銘柄名"],
                code=d["コード"],
                division=d["市場・商品区分"],
                industry_code_1=d['33業種コード'],
                industry_division_1=d['33業種区分'],
                industry_code_2=d['17業種コード'],
                industry_division_2=d['17業種区分'],
                scale_code=d['規模コード'],
                scale_division=d['規模区分']
            ))
    print(added_brand_records)
    if added_brand_records:
        Brand.objects.bulk_create(brand_model_inserts)
        new_brand.to_csv(os.path.join(BASE_DIR, "data", "before_brand.csv"), index=True, header=True)
        print('新規登録あり')
    else:
        print(Brand.objects.all().count())
        print('新規登録なし')


class Command(BaseCommand):
    help = "register TSE brands"

    def add_arguments(self, parser):
        parser.add_argument("first", type=str)

    def handle(self, *args, **options):
        if options["first"] == "aaa":
            reg_brands_from_csv()
        elif options["first"] == "bbb":
            reg_trades_from_csv()
        elif options["first"] == "ccc":
            get_trades_from_stooq()
