import csv
import re

from authentication.models import User
from django.core.management.base import BaseCommand, CommandError
from userprofile.models import FacultyList, MajorList, ProfileList


class Command(BaseCommand):
    help = "Populate user profile details from csv."

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
                    if max(
                        [len(cell.strip()) for cell in row[1:] + [""]]
                    ) == 0 and m.match(row[0]):
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

        for data_dict in models.get("ProfileList", []):
            user = User.objects.get(email=data_dict["owner_email"])
            faculty = FacultyList.objects.get(faculty=data_dict["faculty"])
            major = MajorList.objects.get(major=data_dict["major"])
            m, created = ProfileList.objects.get_or_create(
                owner=user,
                fullname=data_dict["fullname"],
                defaults={
                    "gender": data_dict["gender"],
                    "batch": data_dict["batch"],
                    "faculty": faculty,
                    "major": major,
                },
            )
            if created:
                print("Profile for {} has ben populated".format(data_dict["fullname"]))

        print("Import complete")
