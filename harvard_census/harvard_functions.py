pip install xlrd>=2.0.1
import requests
from bs4 import BeautifulSoup

# Function to get GitHub link from npm
def get_github_link(package_name):
    npm_search_url = f"https://registry.npmjs.org/-/v1/search?text={package_name}&size=1"
    response = requests.get(npm_search_url)

    if response.status_code == 200:
        search_results = response.json().get('objects', [])
        if search_results:
            package_info = search_results[0].get('package')
            if 'links' in package_info and 'repository' in package_info['links']:
                return package_info['links']['repository']
            elif package_name == 'qs':
                # Manually set GitHub link for 'qs' package
                return 'https://github.com/ljharb/qs'
            else:
                # If GitHub link is not present in the response, try to fetch it from the npm package page
                github_link = get_github_link_from_npm_page(package_name)
                return github_link
    return None

# Function to get GitHub link from npm package page
def get_github_link_from_npm_page(package_name):
    npm_page_url = f"https://www.npmjs.com/package/{package_name}"
    response = requests.get(npm_page_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        repository_link = soup.find('a', class_='homepage')
        if repository_link:
            return repository_link['href']

    return None

# Function to check if there is a release for a GitHub repository
def has_github_release(github_link):
    if github_link:
        github_api_url = f"{github_link}/releases/latest"
        response = requests.get(github_api_url)

        try:
            response.raise_for_status()
            if "There aren’t any releases here" not in response.text:
                return True
        except Exception as e:
            print(f"Error checking GitHub release for {github_link}: {e}")

    return False
# Function to get the latest version of a package
def get_latest_version(package_name):
    url = f"https://api.deps.dev/v3alpha/systems/npm/packages/{package_name}"
    response = requests.get(url)

    if response.status_code == 200:
        package_info = response.json()
        versions = package_info.get("versions", [])
        if versions:
            latest_version = max(versions, key=lambda v: v.get('publishedAt'))
            return latest_version
    return None

# Function to get the dependencies for a package's latest version
def get_latest_version_dependencies(package_name, version):
    dependencies_url = f"https://api.deps.dev/v3alpha/systems/npm/packages/{package_name}/versions/{version}:dependencies"
    response = requests.get(dependencies_url)
    
    if response.status_code == 200:
        dependencies = response.json()
        if 'nodes' in dependencies:
            return dependencies['nodes']
    return None

# Function to check if a dependency is signed
def is_dependency_signed(package_name, dependency_name, dependency_version):
    url = f"https://registry.npmjs.org/-/npm/v1/attestations/{dependency_name}@{dependency_version}"
    response = requests.get(url)

    if response.status_code == 200:
        attestation_data = response.json()
        if "error" not in attestation_data:
            return True
    return False
