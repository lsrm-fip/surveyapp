import csv
import re
import random 

from authentication.models import User
from django.core.management.base import BaseCommand, CommandError
from djf_surveys.models import Survey, UserAnswer, Answer

class Command(BaseCommand):
    help = "Generate user's response from csv."

    def add_arguments(self, parser):
        parser.add_argument("--csv", type=str)

    @staticmethod
    def row_to_dict(row, header):
        if len(row) < len(header):
            row += [""] * (len(header) - len(row))
        return dict([(header[i], row[i]) for i, head in enumerate(header) if head])

    def handle(self, *args, **options):
        m = re.compile(r"content:(\w+)")
        header = None
        models = dict()
        try:
            with open(options["csv"]) as csvfile:
                model_data = csv.reader(csvfile)
                for i, row in enumerate(model_data):
                    if max([len(cell.strip()) for cell in row[1:] + [""]]) == 0 and m.match(row[0]):
                        model_name = m.match(row[0]).groups()[0]
                        models[model_name] = []
                        header = None
                        continue

                    if header is None:
                        header = row
                        continue

                    row_dict = self.row_to_dict(row, header)
                    if set(row_dict.values()) == {""}:
                        continue
                    models[model_name].append(row_dict)

        except FileNotFoundError:
            raise CommandError('File "{}" does not exist'.format(options["csv"]))


        value_list = ['tidak_mampu_-_1','kurang_mampu_-_2','cukup_mampu_-_3','mampu_-_4','sangat_mampu_-_5','Sepenuhnya_mampu_-_6']

        for data_dict in models.get("Survey", []):
            user = User.objects.get(email=data_dict["user_email"])
            survey_id = Survey.objects.get(id=data_dict["survey_id"])
            m, object_created = UserAnswer.objects.get_or_create(survey=survey_id, user=user)
            if object_created:
                print("UserAnswer object for {} has been generated".format(data_dict["user_email"]))
            user_answer_id = getattr(m,'id')
            for i in range(14):
                value = random.choice(value_list)
                n, answer_created = Answer.objects.get_or_create(user_answer_id=user_answer_id, question_id = i+1, defaults={"value": value})         
                if answer_created:
                    print("Answers for {} has been generated".format(data_dict["user_email"]))     

        print("Import complete")
