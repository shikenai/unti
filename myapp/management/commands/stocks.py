from django.core.management.base import BaseCommand
import pandas as pd
from unti.settings import BASE_DIR
from myapp.models import Brand
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

def test1(aaa):
    print("run test1")
    print(aaa)
def test2(bbb):
    print("run test2")
    print(bbb)



class Command(BaseCommand):
    help = "register TSE brands"

    def add_arguments(self, parser):
        parser.add_argument("first", type=str)

    def handle(self, *args, **options):
        if options["first"] == "aaa":
            test1()
        elif options["first"] == "bbb":
            test2()
