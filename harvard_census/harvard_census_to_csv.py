import pandas as pd
import csv
from harvard_functions import get_latest_version, get_latest_version_dependencies, is_dependency_signed

# Load the Excel file
excel_file = 'harvard_census_top_100.xlsx'
df = pd.read_excel(excel_file)

# Create and open a CSV file for writing
output_file = 'harvard_package_dependencies_sign.csv'
with open(output_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    # Write the header row
    csvwriter.writerow(["Package", "Version", "Dependency", "Dependency Version", "Relationship", "Signed/Not Signed"])

    # Iterate through the package names from the second column (package name)
    for package in df.iloc[:, 1]:
        latest_version = get_latest_version(package)
        
        if latest_version:
            version = latest_version.get('versionKey', {}).get('version', 'null')
            dependencies = get_latest_version_dependencies(package, version)
            
            if dependencies:
                has_dependencies = False
                for dependency_info in dependencies:
                    relation = dependency_info.get('relation', '')
                    if relation != 'SELF':
                        dependency_name = dependency_info.get('versionKey', {}).get('name', 'unknown')
                        dependency_version = dependency_info.get('versionKey', {}).get('version', 'unknown')
                        signed_status = is_dependency_signed(package, dependency_name, dependency_version)
                        csvwriter.writerow([package, version, dependency_name, dependency_version, relation, signed_status])
                        has_dependencies = True
                if not has_dependencies:
                    # Write a row for the package with "no dependency"
                    csvwriter.writerow([package, version, None, None, None, None])
            else:
                # Write a row for the package with "no dependency"
                csvwriter.writerow([package, version, None, None, None, None])
        else:
            # Write a row for the package that doesn't exist
            csvwriter.writerow([package, None, None, None, None, None])

# Output = package, latest version, dependency, dependency version, relationship, signed/ornot
print(f"Package dependencies have been exported to {output_file}")
