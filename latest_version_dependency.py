import json
from functions import get_latest_version, get_latest_version_dependencies, is_package_signed, is_dependency_signed

# Prompt the user to input an npm package name
package_name = input("Enter the npm package name: ")
latest_version = get_latest_version(package_name)

if latest_version:
    print(f"The latest version of {package_name} is: {latest_version}")
    print("--------------------------------------------------------------------------------")  # Divider
    version = latest_version['versionKey']['version']
    dependencies = get_latest_version_dependencies(package_name, version)

    if dependencies:
        print("Dependencies for this version:")
        formatted_dependencies = json.dumps(dependencies, indent=2)
        print(formatted_dependencies)
        print("--------------------------------------------------------------------------------")  # Divider

        is_signed = is_package_signed(package_name, version)
        if is_signed:
            print(f"{package_name}@{version} is signed. Attestation Data: {is_signed}")
        else:
            print(f"{package_name}@{version} is not signed.")
        print("--------------------------------------------------------------------------------")  # Divider

        # Check the signing status of dependencies
        signed_dependencies = {}
        unsigned_dependencies = {}
        for dependency_name, dependency_version in dependencies.items():
            is_dependency_signed_result = is_dependency_signed(package_name, dependency_name, dependency_version)
            if is_dependency_signed_result:
                signed_dependencies[dependency_name] = dependency_version
            else:
                unsigned_dependencies[dependency_name] = dependency_version

        if signed_dependencies:
            print("Dependencies Signed:")
            print(json.dumps(signed_dependencies, indent=2))
            print("--------------------------------------------------------------------------------")  # Divider

        if unsigned_dependencies:
            print("Dependencies Not Signed:")
            print(json.dumps(unsigned_dependencies, indent=2))
    else:
        print(f"Could not retrieve dependencies for {latest_version}")
else:
    print(f"Could not retrieve information for package {package_name}")
