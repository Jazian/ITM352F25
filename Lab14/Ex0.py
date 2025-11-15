import importlib.util


def check_package_installed(package_name):
    spec = importlib.util.find_spec(package_name)
    return spec is not None


packages = ['scipy', 'statsmodels', 'matplotlib']


for pkg in packages:
    if check_package_installed(pkg):
        print(f"{pkg} is installed ✅")
    else:
        print(f"{pkg} is NOT installed ❌")
