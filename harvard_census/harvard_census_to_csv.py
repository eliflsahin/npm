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
                        csvwriter.writerow([f"{package}{version}", f"{dependency_name}{dependency_version}", signed_status])
                        has_dependencies = True
                if not has_dependencies:
                    csvwriter.writerow([f"{package}{version}", "no dependency"])
            else:
                csvwriter.writerow([f"{package}{version}", "no dependency"])
        else:
            csvwriter.writerow([f"{package}", "no dependency"])

# Output = package(latestversion), dependency(version), signed/ornot
print(f"Package dependencies have been exported to {output_file}")
