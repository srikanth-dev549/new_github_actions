#Creates a json file with all the projects ===> roles ===> principles (Example data.json attached)
import json
import subprocess
import os
from deepdiff import DeepDiff

# Project IDs are stored in the list format
project_id = "new-project2-376506"

all_projects_roles_principles = [] # Storing all the projects with roles and principles as a list
project_to_users = {} # Dictionary to map project ID as key and user_role
final_out = {}
# Looping through all the projects to get the iam policies for a project in json format

ids = f"gcloud projects get-iam-policy {project_id} --format=json"
bind = subprocess.check_output(ids, shell=True)
iam_roles = json.loads(bind.decode())
# Debug to print all the bindings list of members and the roles that are attached to the members
print(iam_roles)
role_to_principle_dict = {}  # Dictionary to store role as key and principles(list) as value
# Looping through the bindings for a specific roles and storing the emails in principles list
for member in iam_roles['bindings']:
    principles_list = []  # List of all the principles for a specific role
    # Looping through all the members i.e., principles
    for principle in member['members']:
        # Organization roles are omitted here
        if "organization" in member['role']:
            pass
        # Emails will be appended to the principles list
        # Roles will be mapped to the principles list and stored in dictionary role_to_principle_dict
        else:
            principles_list.append(principle)
            role_to_principle_dict[member['role'].replace("roles/", "")] = principles_list
# the role_to_principle_dict will be stored in project_to_users dictionary with project ID as key and role_to_principle_dict as value
project_to_users[f'{project_id}'] = role_to_principle_dict
# Appending all the projects as a list with roles and principles
all_projects_roles_principles.append(project_to_users)
# Creating dictionary under user_roles as key and all_projects_roles_principles as key
final_out['user_roles'] = all_projects_roles_principles
# Debug the final dictionary which has all the projects, roles and principles
print(final_out)
filename = f'{project_id}-data.json'
roles_added_manually = {}
if os.path.isfile(filename):
    print("The file exists reconciling with existing commits and changes made in the console")
    with open(f'{project_id}-data.json', 'r') as f:
        data = json.load(f)
    differences = {}
    # check if final_out has any new keys that are not in data
    for key, value in final_out['user_roles'][0][project_id].items():
        if key not in data['user_roles'][0][project_id]:
            differences[key] = final_out['user_roles'][0][project_id][key]
        # check if final_out has any new values that are not in data
        for val in final_out['user_roles'][0][project_id][key]:
            if val not in data['user_roles'][0][project_id][key]:
                differences[key] = val
    print("Reconciliation successful.")
    print(differences)
    if not differences:
        print("No changes were made in the gcp console running terraform plan for the commits done to data.json")
    else:
        print(f'{differences} were created in the console')
        raise ValueError("Roles shown above are created in the console exiting the pipeline")
else:
    print("No data.json file present run the pipeline manually to create data.json")
