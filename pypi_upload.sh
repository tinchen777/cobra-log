
mv dist/* history/

python -m build

twine upload dist/*
