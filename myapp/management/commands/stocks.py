from django.core.management.base import BaseCommand
import pandas as pd
from app.models import Brand
from test.settings import BASE_DIR


def test():
    df = pd.read_csv(BASE_DIR.parent / "data/brand.csv")
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


class Command(BaseCommand):
    help = "register TSE brands"

    def handle(self, *args, **options):
        test()
