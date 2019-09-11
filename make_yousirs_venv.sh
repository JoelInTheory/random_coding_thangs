py3venv_dir="${PWD}/py3venv"
python3 -m venv ${py3venv_dir}
source ${py3venv_dir}/bin/activate
echo "using virtual env: $(which python)"
read -p "if that doesn't look right you should probably control-c outta here, otherwise press enter to continue"
pip install -r requirements.txt
