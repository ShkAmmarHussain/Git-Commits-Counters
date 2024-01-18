import gitlab
import os
import git
import stat
import shutil
import re

def sanitize_path(path):
    """Replace invalid characters in the path"""
    return re.sub(r'[<>:"/\\|?*]', '_', path)

def remove_readonly(func, path, _):
    """Change file to editable"""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def delete_directory(directory_path):
    """Delete Cloned Repo"""
    try:
        # Set up the callback function to handle read-only files
        shutil.rmtree(directory_path, onerror=remove_readonly)
        print(f"Successfully deleted the directory: {directory_path}")
    except Exception as e:
        print(f"Error deleting the directory: {e}")

def cleanup_invalid_paths(repo_path):
    """Remove invalid paths from the repository"""
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            if ":Zone.Identifier" in file_path:
                os.remove(file_path)
                print(f"Removed invalid path: {file_path}")

def sanitize_invalid_paths(repo_path):
    """Replace invalid characters in file and directory names"""
    for root, dirs, files in os.walk(repo_path):
        for directory in dirs:
            dir_path = os.path.join(root, directory)
            sanitized_path = sanitize_path(dir_path)
            if sanitized_path != dir_path:
                os.rename(dir_path, sanitized_path)
                print(f"Renamed invalid directory path: {dir_path} to {sanitized_path}")

        for file in files:
            file_path = os.path.join(root, file)
            sanitized_path = sanitize_path(file_path)
            if sanitized_path != file_path:
                os.rename(file_path, sanitized_path)
                print(f"Renamed invalid file path: {file_path} to {sanitized_path}")


def set_git_config_protectNTFS(repo_path):
    """Set git configuration to ignore NTFS naming restrictions"""
    repo = git.Repo(repo_path)
    repo.git.config('core.protectNTFS', 'false')


def count_commits(project):
    """Counting Commits for a GitLab project"""

    # set_git_config_protectNTFS()  # Set git configuration

    repo = git.Repo.clone_from(project, "temp_repo", sparse=False)  # Clone the repository

    set_git_config_protectNTFS("temp_repo")  # Set git configuration
    # Initialize a dictionary to store commit counts and users
    commit_info = {}

    # Iterate over all branches
    for branch in repo.remote().refs:
        branch_name = branch.name.split("/")[-1]

        # Check if the local branch already exists
        if repo.heads.__contains__(branch_name):
            # If it does, just checkout the existing branch
            repo.git.checkout(branch_name, force=True)
        else:
            # If it doesn't, create a new local branch for each remote branch
            repo.create_head(branch_name, branch)
            repo.git.checkout(branch_name, force=True)  # Checkout the branch

        commits = list(repo.iter_commits(branch_name))

        # Initialize a dictionary for the current branch
        branch_info = {'commits': len(commits), 'users': {}}

        # Iterate over commits in the current branch
        for commit in commits:
            author = commit.author.email
            if author not in branch_info['users']:
                branch_info['users'][author] = 1
            else:
                branch_info['users'][author] += 1

        # Store the branch information in the overall dictionary
        commit_info[branch_name] = branch_info

    # Close the repo
    repo.close()

    # Clean up the temporary repository
    delete_directory("temp_repo")
    # try:
    #     delete_directory("temp_repo")
    # except:
    #     sanitize_invalid_paths("temp_repo")

    return commit_info


def process_gitlab_group(group_path, token):
    """Process a GitLab group and count commits for each project"""
    gl = gitlab.Gitlab('https://gitlab.com', private_token=token)
    group = gl.groups.get(group_path)

    results = {}
    for project in group.projects.list(all=True):
        project_dict = project.asdict()
        results[project_dict['name']] = count_commits(project_dict['http_url_to_repo'])
        # print(project.asdict()['name'])
        

    return results

if __name__ == "__main__":
    # Provide your GitLab group path and API token
    gitlab_group_path = ""
    gitlab_token = ""

    # Process GitLab group and print results
    results = process_gitlab_group(gitlab_group_path, gitlab_token)

    # Print the commit information for each project and branch
    for project_name, commit_info in results.items():
        print(f"Project: {project_name}")
        for branch, info in commit_info.items():
            print(f"  Branch: {branch}")
            print(f"    Commits:")
            for user, commit_count in info['users'].items():
                print(f"      {user}: {commit_count} commits")
            print()
