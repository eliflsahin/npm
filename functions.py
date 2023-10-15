import requests

def get_latest_version(package_name):
    url = f"https://api.deps.dev/v3alpha/systems/npm/packages/{package_name}"
    response = requests.get(url)

    if response.status_code == 200:
        package_info = response.json()
        versions = package_info.get("versions", [])
        latest_version = max(versions, key=lambda v: v.get('publishedAt'))
        return latest_version
    else:
        return None

def get_latest_version_dependencies(package_name, version):
    dependencies_url = f"https://api.deps.dev/v3alpha/systems/npm/packages/{package_name}/versions/{version}:dependencies"
    response = requests.get(dependencies_url)
    
    if response.status_code == 200:
        dependencies = response.json()
        if 'edges' in dependencies:
            del dependencies['edges']
        return dependencies
    else:
        return None

def is_package_signed(package_name, version):
    url = f"https://registry.npmjs.org/-/npm/v1/attestations/{package_name}@{version}"
    response = requests.get(url)

    if response.status_code == 200:
        attestation_data = response.json()
        if "error" not in attestation_data:
            return attestation_data
        else:
            return None
    else:
        return None

def is_dependency_signed(package_name, dependency_name, dependency_version):
    url = f"https://registry.npmjs.org/-/npm/v1/attestations/{dependency_name}@{dependency_version}"
    response = requests.get(url)

    if response.status_code == 200:
        attestation_data = response.json()
        if "error" not in attestation_data:
            return attestation_data
        else:
            return None
    else:
        return None
