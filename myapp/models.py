from django.db import models


class Brand(models.Model):
    nation = models.CharField(max_length=30, blank=True, null=True, verbose_name='国')
    market = models.CharField(max_length=20, blank=True, null=True)
    brand_name = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=5, blank=True, null=True)
    division = models.CharField(max_length=20, blank=True, null=True)
    industry_code_1 = models.CharField(max_length=10, blank=True, null=True)
    industry_division_1 = models.CharField(max_length=10, blank=True, null=True)
    industry_code_2 = models.CharField(max_length=10, blank=True, null=True)
    industry_division_2 = models.CharField(max_length=10, blank=True, null=True)
    scale_code = models.CharField(max_length=10, blank=True, null=True)
    scale_division = models.CharField(max_length=10, blank=True, null=True)

    def unique_code(self):
        return "【" + self.nation + "：" + self.market + "】" + self.brand_name + "(" + str(self.code) + "）"

    def __str__(self):
        return self.brand_name + "(" + self.market + ":" + str(self.code) + ")"


class Trades(models.Model):
    brand = models.ForeignKey(to=Brand, on_delete=models.CASCADE)
    brand_code = models.CharField(max_length=30, null=True, blank=True)
    trade_date = models.DateField(blank=True, null=True)
    open_value = models.FloatField(verbose_name='始値', blank=True, null=True)
    close_value = models.FloatField(verbose_name='終値', blank=True, null=True)
    high_value = models.FloatField(verbose_name='高値', blank=True, null=True)
    low_value = models.FloatField(verbose_name='安値', blank=True, null=True)
    volume = models.IntegerField(verbose_name='出来高', blank=True, null=True)

    def __str__(self):
        return "取引" + self.brand.unique_code() + self.trade_date.strftime("%Y年%m月%d日")