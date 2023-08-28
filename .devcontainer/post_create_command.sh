pip install -r /workspaces/orm_test/requirements.txt
cp /workspaces/orm_test/project.pth $(python -c 'import site; print(site.getsitepackages()[0])')
cat ./.devcontainer/.bashrc > ~/.bashrc