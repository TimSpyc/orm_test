pip install -r /workspaces/orm_test/requirements.txt
cat ./.devcontainer/.bashrc >> ~/.bashrc
cp /workspaces/orm_test/project.pth $(python -m site --user-site)/project.pth
cd orm_test
python manage.py migrate
python ../example_db/fill_db.py