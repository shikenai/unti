import math

from django.core.management.base import BaseCommand
import pandas as pd
from unti.settings import BASE_DIR
from myapp.models import Brand, Trades
import time
from django_pandas.io import read_frame
import datetime
import numpy as np


# def compare_2_columns(column1, column2):
#     if column1 > column2:
#         return row[]


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


def compare_2columns(df, column1, column2):
    df["{}_minus_{}".format(column1, column2)] = df[column1] - df[column2]


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
    hist_rate = hist / prices
    return macd, signal, hist, hist_rate


def set_macd(df):
    df['macd_line'], df['macd_signal'], df['macd_hist'], df['macd_hist_rate'] = calc_macd(df.close_value, 12, 26, 9)
    return df


# ------MACD---end-------
def operate_single_column(df, column, **kwargs):
    # 指定した一つの列に対して、前日との差分及びその率並びに移動平均を取得するもの
    # 使用例：一昨日と昨日の終値の異動、異動/終値（終値からみて、どの程度異動したのか）
    if kwargs.get('diff'):
        df["diff_{}".format(column)] = df[column].diff()
    if kwargs.get('diff_pct'):
        df["diff_pct_{}".format(column)] = df[column].pct_change()
    if kwargs.get('ma_span'):
        for span in kwargs['ma_span']:
            df["{}MA_{}".format(span, column)] = df[column].rolling(span).mean()


def operate_double_columns(df, column1, column2, **kwargs):
    if kwargs.get('size_comparison'):
        df["{}_gt_{}".format(column1, column2)] = df[column1] - df[column2]


def set_gdx(row, short, long, name):
    new_column = "trend_by_{}".format(name)
    # short（短期）が上昇
    if row[short] > 0:
        # 短期上昇
        if row[long] < 0:
            row[new_column] = "買い"
        else:
            if row[short] >= row[long]:
                # 短期の上昇が長期の上昇より強い
                row[new_column] = "まだ上昇"
            else:
                # 短期の上昇が長期の上昇よりも緩い
                row[new_column] = "注意"
    else:
        # 短期が下降
        if row[long] > 0:
            row[new_column] = "下降！"
        else:
            if row[short] > row[long]:
                row[new_column] = '好転？'
            else:
                row[new_column] = 'まだまだ暗黒'
    return row


def test():
    _trades = Trades.objects.filter(brand_code="1808.jp").order_by("Date")
    n = _trades.count()
    x = 10000
    if n < x:
        n_minus = 0
    else:
        n_minus = n - x
    df = read_frame(_trades.all()[n_minus:n])
    # # Close列に対して、変化推移、変化率、３日移動平均、２５日移動平均を追加
    operate_single_column(df, "Close", diff=True, diff_pct=True, ma_span=[3, 25])
    operate_double_columns(df, "3MA_Close", "25MA_Close", size_comparison=True)
    df = df.apply(set_gdx, args=("3MA_Close", "25MA_Close", 'MA'), axis=1)
    operate_single_column(df, '3MA_Close_gt_25MA_Close', ma_span=[3])

    # df = set_ichimoku_cloud(df)
    # df = df.apply(set_sanyaku, axis=1)
    # df = set_macd(df)
    # pd.set_option('display.max_columns', df.shape[1])

    # df = df[["brand", "brand_code", "Date", "Close"]]
    # n = -5
    # df["shift"] = df["Close"].shift(n)
    # df["shift_max"] = df["Close"].shift(n).rolling(n // 2 - n, center=True).max()

    df = df[26:]
    df = df.reset_index(drop=True)
    # print(df['2023-01-01': '2023-02-02'])
    col_num = df.columns.get_loc('Close')
    n = 21
    index_num = df.shape[0]
    max_list = []
    for i in range(index_num):
        if i + n <= index_num:
            max_list.append(df.iloc[i:i + n, [col_num]].max().max())
        else:
            max_list.append(np.nan)
    print(max_list)
    print(len(max_list))
    for j in range(len(max_list)):
        print(j)
        print(max_list[j])
    df["{}日後までの最大値".format(n)] = max_list

    return df.T


class Command(BaseCommand):
    help = "register TSE brands"

    def add_arguments(self, parser):
        parser.add_argument("first", type=str)

    def handle(self, *args, **options):
        test()
