py3venv_dir="${PWD}/py3venv"
python3 -m venv ${py3venv_dir}
source ${py3venv_dir}/bin/activate
pip freeze
pip install -r requirements.txt
