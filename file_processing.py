import os
import uuid
import subprocess

def clone_github_repo(github_url, local_path):
    try:
        #subprocess.run(['cd', local_path], check=True)
        # local_path = os.getcwd() + "/" + local_path
        #print("local path: ", local_path)
        cmd = "git clone " + github_url
        #subprocess.run(['git', 'clone', github_url], cwd=local_path, check=True)
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone repository: {e}")
        return False
