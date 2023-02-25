from django.core.management.base import BaseCommand
import pandas as pd
from unti.settings import BASE_DIR
from myapp.models import Brand, Trades
import time
import pandas_datareader.data as data
import datetime as dt
import os
from django_pandas.io import read_frame


# ----------ここからシステム環境再構築時に使用するもの----------
def reg_brands_from_csv():
    # システム環境再構築時に使うことを想定
    # djangoで吐き出したcsvを新規プロジェクトに移築する時に使ってください
    # とりあえず旧プロジェクトで吐き出したcsvをdataframeとして取得
    df = pd.read_csv(BASE_DIR / "data/brand.csv")
    # よくわからんけど、ググった結果、to_dict(orient='records')すれば良いらしい
    de_records = df.to_dict(orient='records')
    # あとでbulk_createする際に使用する空のリスト
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
    # システム環境再構築時に使うことを想定
    # djangoで吐き出したcsvを新規プロジェクトに移築する時に使ってください
    # とりあえず旧プロジェクトで吐き出したcsvをdataframeとして取得
    df = pd.read_csv(BASE_DIR / "data/trade.csv")
    # よくわからんけど、ググった結果、to_dict(orient='records')すれば良いらしい
    de_records = df.to_dict(orient='records')
    # あとでbulk_createする際に使用する空のリスト
    model_inserts = []
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
    Trades.objects.bulk_create(model_inserts)


# ----------ここまでシステム環境再構築時に使用するもの----------

# ----------ここから日々の取引データ取得に関するもの----------
def get_trades_from_stooq():
    print('from stppq')
    t1 = time.time()
    # list_brand_code = df["brand_code"].to_list()
    # list_trade_date= df["trade_date"].to_list()
    # _df = df["trade_date"].sort_values().drop_duplicates().to_list()
    # dict_tradedate_brandcode = {}

    # get_target_brands("jp")[0] は、既にある程度の取引状況をデータとして保有しているもの
    # →各銘柄ごとの、取引最終日を取得し、その日以降のデータを取得する必要がある
    owned_brands = get_target_brands('jp')[0]
    print(owned_brands)
    # いい感じ
    # df = read_frame(Trades.objects.all().order_by("trade_date"))
    # df = df[["trade_date", "brand_code"]].groupby("brand_code").max()
    # df = df.reset_index()
    # target_trade_date_list = df["trade_date"].sort_values().drop_duplicates().to_list()
    # returning_list = []
    # for i in range(len(target_trade_date_list)):
    #     a = df[df["trade_date"] == target_trade_date_list[i]]["brand_code"].to_list()
    #     returning_list.append({target_trade_date_list[i]: a})
    # print(returning_list)
    # いい感じ

    # →全ての銘柄について、一律指定した日からデータ取得日までのデータを取得すれば良い
    # print("8888.jp" in get_target_brands("jp")[0])
    # new_brands = get_target_brands('jp')[1]
    # ここはもう一括でstooqから取得すれば良いので楽
    print(time.time() - t1)


def sort_out_2lists(list1, list2):
    # get_target_brands関数で使用するもの
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
    # 取引情報を取得するにあたり、①既にある程度取引情報を持っている銘柄　②全く取引情報を持っていない銘柄　の２種類で
    # 処理方法を分ける必要があるため、①と②を分ける処理を行う。
    # この際、自作関数sort_out_2_listsを使用する。
    # returnの一つ目は、２つのリストの交わる部分、二つ目はリスト１にのみ存在する部分、三つ目はリスト２にのみ存在する部分
    # なお、将来海外銘柄を取り扱う可能性を考慮し、引数としてnationをもつ。日本株の場合は一律"jp"

    # 最新の銘柄リスト
    list_csv_brand = list(pd.read_csv(BASE_DIR / "data/before_brand.csv")["コード"])  # ここでは数値として取得しているみたい
    list_csv_brand_str = [str(c) + "." + nation for c in list_csv_brand]  # だから文字列に変換する
    # tradesに登録済の銘柄リスト
    brands_in_trades = list(Trades.objects.all().order_by("brand_code").distinct().values_list('brand_code', flat=True))

    return sort_out_2lists(list_csv_brand_str, brands_in_trades)[0], \
        sort_out_2lists(list_csv_brand_str, brands_in_trades)[1], sort_out_2lists(list_csv_brand_str, brands_in_trades)[
        2]


# ----------ここまで日々の取引データ取得に関するもの----------

# ----------ここから東証一部上場企業の銘柄データ取得に関するもの----------
def get_tse_brands():
    # 東証から銘柄データを取得し、before_brand.csvとして全体を格納。この際、登録されていない銘柄は一括登録する。
    # 毎月１回やればいいのかなぁと思うけど、そんなに大したことはしてないので、毎日日付変わった時点に実行すればヨシ
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


# ----------ここまで東証一部上場企業の銘柄データ取得に関するもの----------

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
