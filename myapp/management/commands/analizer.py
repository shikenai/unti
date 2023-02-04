from django.core.management.base import BaseCommand
import pandas as pd
from unti.settings import BASE_DIR
from myapp.models import Brand, Trades
import time
from django_pandas.io import read_frame
import datetime


def set_gdx(row):
    # 短期移動平均線と長期移動平均線をみて、ゴールデンクロスかデッドクラスかをbooleanで判定
    if row["short_MA"] > row["long_MA"]:
        row["gdx"] = True
    else:
        row["gdx"] = False
    return row


def set_sanyaku(row):
    if row["conversion_line"] > row["base_line"] and row["lagging_span"] > row["close_value"] > row["leading_span1"] and row["close_value"] > row["leading_span2"]:
        row["sanyaku"] = True
    elif row["conversion_line"] < row["base_line"] and row["lagging_span"] < row["close_value"] < row[
            "leading_span1"] and row["close_value"] < row["leading_span2"]:
        row["sanyaku"] = False
    else:
        row["sanyaku"] = None
    if row["close_value"] > row["leading_span1"] and row["close_value"] > row["leading_span2"]:
        row["over_cloud"] = True
    elif row["close_value"] < row["leading_span1"] and row["close_value"] < row["leading_span2"]:
        row["over_cloud"] = False
    else:
        row["sanyaku"] = None
    return row


def set_ichimoku_cloud(df):
    # 一目均衡表に関するデータを作成
    additional_dates = pd.date_range(
        start=df["trade_date"].max() + datetime.timedelta(days=1),
        end=df["trade_date"].max() + datetime.timedelta(days=25),
    )

    df = pd.concat([df, pd.DataFrame(additional_dates, columns=["trade_date"])], ignore_index=True)
    # 基準線
    high26 = df["high_value"].rolling(window=26).max()
    low26 = df["low_value"].rolling(window=26).min()
    df["base_line"] = (high26 + low26) / 2
    # 転換線
    high9 = df["high_value"].rolling(window=9).max()
    low9 = df["low_value"].rolling(window=9).min()
    df["conversion_line"] = (high9 + low9) / 2
    # 先行スパン1
    leading_span1 = (df["base_line"] + df["conversion_line"]) / 2
    df["leading_span1"] = leading_span1.shift(25)

    # 先行スパン2
    high52 = df["high_value"].rolling(window=52).max()
    low52 = df["low_value"].rolling(window=52).min()
    leading_span2 = (high52 + low52) / 2
    df["leading_span2"] = leading_span2.shift(25)

    # 遅行スパン
    df["lagging_span"] = df["close_value"].shift(-25)

    return df


def test():
    _trades = Trades.objects.filter(brand_code="7203.jp").order_by("trade_date")
    n = _trades.count()
    x = 3000
    if n < x:
        n_minus = 0
    else:
        n_minus = n - x
    df = read_frame(_trades.all()[n_minus:n])
    df["short_MA"] = df["close_value"].rolling(3).mean()
    df["long_MA"] = df["close_value"].rolling(25).mean()
    df["diff_close_value"] = df["close_value"].diff()
    df["diff_close_value_rate"] = df["close_value"].pct_change()
    pd.set_option('display.max_columns', df.shape[1])
    df = df.apply(set_gdx, axis=1)
    df = set_ichimoku_cloud(df)
    df = df.apply(set_sanyaku, axis=1)
    print(df)


class Command(BaseCommand):
    help = "register TSE brands"

    def add_arguments(self, parser):
        parser.add_argument("first", type=str)

    def handle(self, *args, **options):
        test()
