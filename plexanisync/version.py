import configparser


def version():
    pyproject = configparser.ConfigParser()
    pyproject.read('pyproject.toml', encoding="utf-8")
    return pyproject['tool.poetry']['version']
