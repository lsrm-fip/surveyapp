import numpy as np
import math
from django.db import transaction
from django.core.management.base import BaseCommand
from authentication.models import User
from django.contrib.auth.hashers import make_password


user_num = 30
list = []


def user_list():
    num_arr = np.arange(1, user_num + 1)
    for i in num_arr:
        list.append("user%s@gmail.com" % i)
    return list


user_list = user_list()


class Command(BaseCommand):
    help = "Generates dummy data for testing"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        exclude_email = ["farhanhamidlubis@gmail.com"]
        user = User.objects.all().exclude(email="farhanhamidlubis@gmail.com")
        user.delete()

        self.stdout.write("Creating dummy data...")

        User.objects.bulk_create(
            [
                User(
                    email=email,
                    password=make_password(password="master"),
                    is_active=True,
                )
                for email in user_list
            ]
        )

        print(User.objects.all())
