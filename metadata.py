import toml
import os
WORKDIR = os.path.dirname(__file__)


with open(os.path.join(WORKDIR,'pyproject.toml'), 'r') as file:
    data = toml.load(file)
project_name = data['project']['name']
version = data['project']['version']