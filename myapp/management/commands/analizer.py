from django.core.management.base import BaseCommand
import pandas as pd
from unti.settings import BASE_DIR
from myapp.models import Brand, Trades
import time
from django_pandas.io import read_frame
import datetime
import numpy as np


def set_gdx(row):
    # 短期移動平均線と長期移動平均線をみて、ゴールデンクロスかデッドクラスかをbooleanで判定
    if row["short_MA"] > row["long_MA"]:
        row["gdx"] = True
    else:
        row["gdx"] = False
    return row


def set_sanyaku(row):
    # set_ichimoku_cloud()後に使用するもの。三役好転か、三役暗転かどうかを判定する
    if row["conversion_line"] > row["base_line"] and row["lagging_span"] > row["close_value"] > row["leading_span1"] and \
            row["close_value"] > row["leading_span2"]:
        row["sanyaku"] = True
    elif row["conversion_line"] < row["base_line"] and row["lagging_span"] < row["close_value"] < row[
        "leading_span1"] and row["close_value"] < row["leading_span2"]:
        row["sanyaku"] = False
    else:
        row["sanyaku"] = None
    # set_ichimoku_cloud()後に使用するもの。終値が雲の上にあるのか下にあるのかを判定する
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


def set_ma(df, short_span, long_span):
    df["short_MA"] = df["close_value"].rolling(short_span).mean()
    df["long_MA"] = df["close_value"].rolling(long_span).mean()
    return df


def set_close_diff(df):
    # 日々の終値の差分を抽出するとともに、その割合を計算
    df["diff_close_value"] = df["close_value"].diff()
    df["diff_close_value_rate"] = df["close_value"].pct_change()
    return df


# ------MACD--start------
# 指数平滑移動平均計算
def calc_ema(prices, period):
    ema = np.zeros(len(prices))
    ema[:] = np.nan  # NaN で初期化
    ema[period - 1] = prices[:period].mean()  # 最初だけ単純移動平均
    for d in range(period, len(prices)):
        ema[d] = ema[d - 1] + (prices[d] - ema[d - 1]) / (period + 1) * 2
    return ema


# MACD 計算
def calc_macd(prices, period_short, period_long, period_signal):
    ema_short = calc_ema(prices, period_short)
    ema_long = calc_ema(prices, period_long)
    macd = ema_short - ema_long  # MACD = 短期移動平均 - 長期移動平均
    signal = pd.Series(macd).rolling(period_signal).mean()  # シグナル = MACD の移動平均
    hist = macd - signal
    return macd, signal, hist


def set_macd(df):
    df['macd_line'], df['macd_signal'], df['macd_hist'] = calc_macd(df.close_value, 12, 26, 9)
    return df

# ------MACD---end-------


def test():
    _trades = Trades.objects.filter(brand_code="7203.jp").order_by("trade_date")
    n = _trades.count()
    x = 100
    if n < x:
        n_minus = 0
    else:
        n_minus = n - x
    df = read_frame(_trades.all()[n_minus:n])
    # df = set_ma(df, 3, 26)
    # df = df.apply(set_gdx, axis=1)
    # df = set_close_diff(df)
    # df = set_ichimoku_cloud(df)
    # df = df.apply(set_sanyaku, axis=1)
    df = set_macd(df)
    pd.set_option('display.max_columns', df.shape[1])
    print(df)
    # print(df.head(30))
    # print("----------------------")
    # print(df.tail(30))


class Command(BaseCommand):
    help = "register TSE brands"

    def add_arguments(self, parser):
        parser.add_argument("first", type=str)

    def handle(self, *args, **options):
        test()
