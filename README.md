# Surveyapp

## Website pengembangan layanan survey untuk mengukur resiliensi akademik mahasiwa di lingkungan kampus Universitas Negeri Medan

Setting Up:
1. Create venv
2. Install requirements
3. Start project and apps
4. Copy templates and static files
5. Makemigrations and migrate
6. Distribute university data: 
	python manage.py load_univ_data --csv userprofile/univ_data.csv
7. Copy database db.sqlite3 --> consist of survey data
8. Overwrite modified djf_surveys library to current djf_surveys folder
9. Done

To populate dummy samples:
1. Create users model:\
	python manage.py gen_dummy_users (set the number of user in the code)
2. Append users properties:\
	python manage.py gen_user_profile --csv userprofile/user_profile.csv
3. Create UserAnswer object and append users answers:\
	python manage.py gen_user_response --csv summary/user_response.csv

Deployement:
1. Git clone 
2. Install requirements
3. Collectstatic
4. Copy database and .env file
5. Makemigrations and migrate
7. Overwrite modified djf_surveys library to current djf_surveys folder --> use tar and unzip
8. Change allowed host and set Debug to False
