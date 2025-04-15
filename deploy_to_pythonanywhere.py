import sys
import os
import requests

# PythonAnywhere credentials and configuration
username = os.environ.get('PA_USERNAME')
api_token = os.environ.get('PA_API_TOKEN')
domain_name = f"{username}.pythonanywhere.com"

api_base = f"https://www.pythonanywhere.com/api/v0/user/{username}/"
headers = {'Authorization': f'Token {api_token}'}

# Function to reload PythonAnywhere web app
def reload_webapp():
    response = requests.post(
        f"{api_base}webapps/{domain_name}/reload/",
        headers=headers
    )
    if response.status_code == 200:
        print("Web app reloaded successfully")
        return True
    else:
        print(f"Failed to reload web app: {response.status_code} {response.text}")
        return False

# Function to update files on PythonAnywhere
def update_files_from_github():
    # Get the git repo URL from command line args or environment
    github_repo = os.environ.get('GITHUB_REPO')
    if not github_repo:
        print("Error: GitHub repository URL not provided")
        return False
        
    # Command to pull latest changes from GitHub
    command = f"cd ~/sample-project && git pull"
    
    response = requests.post(
        f"{api_base}consoles/",
        headers=headers,
        json={"executable": "bash", "arguments": "-c \"" + command + "\""}
    )
    
    if response.status_code == 201:
        console_id = response.json()["id"]
        print(f"Console created with ID: {console_id}")
        print("Files updated from GitHub")
        return True
    else:
        print(f"Failed to create console: {response.status_code} {response.text}")
        return False

# Main execution
if __name__ == "__main__":
    if update_files_from_github():
        reload_webapp()