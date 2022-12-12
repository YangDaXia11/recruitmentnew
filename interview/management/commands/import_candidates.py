import csv
from interview.models import Candidate
from django.core.management import BaseCommand


# 要求实现功能是将一个csv文件的内容种读取候选人列表，导入到数据库种
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)  # liunx用法，“--”表示长命令,设置分隔符为;

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt') as f:
            reader = csv.reader(f, dialect='excel', delimiter=';')
            for row in reader:
                candite = Candidate.objects.create(
                    username=row[0],
                    city=row[1],
                    phone=row[2],
                    bachelor_school=row[3],
                    major=row[4],
                    degree=row[5],
                    test_score_of_general_ability=row[6],
                    paper_score=row[7],
                )
                # print(candite)
# D:\django\recruitmentnew\candidates.csv
