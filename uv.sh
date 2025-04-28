uv python install 3.12 
uv venv --python 3.12
source .venv/Scripts/activate
uv init
uv add jupyter ipykernel pandas matplotlib python-dotenv
echo "DONE!"