import csv
import re

from django.core.management.base import BaseCommand, CommandError
from userprofile.models import FacultyList, MajorList


class Command(BaseCommand):
    help = "Load university faculty and major data from a CSV file."

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

        for data_dict in models.get("FacultyList", []):
            f, created = FacultyList.objects.get_or_create(faculty=data_dict["faculty_name"])

            if created:
                print('Created Faculty "{}"'.format(f.faculty))

        for data_dict in models.get("MajorList", []):
            faculty = FacultyList.objects.get(faculty=data_dict["faculty_name"])
            m, created = MajorList.objects.get_or_create(major=data_dict["major_name"],faculty=faculty,)
            if created:
                print('Created Major "{}"'.format(data_dict["major_name"]))

        print("Import complete")
 