import io
from django.core.management.base import BaseCommand
import matplotlib
import matplotlib.pyplot as plt
from django.http import HttpResponse

# バックエンドを指定
# matplotlib.use('Agg')


# グラフ作成
def set_plt():
    x = ["07/01", "07/02", "07/03", "07/04", "07/05", "07/06", "07/07"]
    y = [3, 5, 0, 5, 6, 10, 2]
    plt.bar(x, y, color='#00d5ff')
    plt.title(r"$\bf{Running Trend  -2020/07/07}$", color='#3407ba')
    plt.xlabel("Date")
    plt.ylabel("km")


# SVG化
def plt2svg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    print(s)
    buf.close()
    return s


# 実行するビュー関数
def get_svg():
    set_plt()
    svg = plt2svg()  # SVG化
    plt.cla()  # グラフをリセット
    response = HttpResponse(svg, content_type='image/svg+xml')
    res_str = response.content.decode('utf-8')
    return res_str


# BaseCommandを継承して作成
class Command(BaseCommand):
    help = "register TSE brands"

    def add_arguments(self, parser):
        parser.add_argument("first", type=str)

    def handle(self, *args, **options):
        get_svg()
