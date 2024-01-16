# import git
# import os, shutil, stat


# def remove_readonly(func, path, _):
#     os.chmod(path, stat.S_IWRITE)
#     func(path)

# def delete_directory(directory_path):
#     try:
#         # Set up the callback function to handle read-only files
#         shutil.rmtree(directory_path, onerror=remove_readonly)
#         print(f"Successfully deleted the directory: {directory_path}")
#     except Exception as e:
#         print(f"Error deleting the directory: {e}")

# def count_commits(remote_url, filter_branches):
#     repo = git.Repo.clone_from(remote_url, "temp_repo")  # Clone the repository

#     # Initialize a dictionary to store commit counts and users
#     commit_info = {}

#     # Iterate over branches
#     for remote_branch in repo.remote().refs:
#         branch_name = remote_branch.name.split("/")[-1]

#         # Check if the branch should be filtered
#         if branch_name not in filter_branches:
#             continue

#         # Check if the local branch already exists
#         if branch_name not in repo.heads:
#             repo.create_head(branch_name, remote_branch)  # Create a new local branch for each remote branch

#         repo.git.checkout(branch_name)  # Checkout the branch

#         commits = list(repo.iter_commits(branch_name))

#         # Initialize a dictionary for the current branch
#         branch_info = {'commits': len(commits), 'users': {}}

#         # Iterate over commits in the current branch
#         for commit in commits:
#             author = commit.author.email
#             if author not in branch_info['users']:
#                 branch_info['users'][author] = 1
#             else:
#                 branch_info['users'][author] += 1

#         # Store the branch information in the overall dictionary
#         commit_info[branch_name] = branch_info

#     # Close the repo
#     repo.close()

#     # Clean up the temporary repository
#     delete_directory("temp_repo")
#     # shutil.rmtree("temp_repo")  # Use shutil.rmtree for cleanup

#     return commit_info

# if __name__ == "__main__":
#     # remote_url = "https://gitlab.com/Codistan/bizb/seller-admin.git"  # Replace with your repository URL
#     # filter_branches = ['staging', 'master']  # Add branches to filter
    
#     remote_url = "https://gitlab.com/Codistan/artificial-intelligence/qaiser-test-task.git"
#     filter_branches = ['dev', 'test']
#     commit_info = count_commits(remote_url, filter_branches)

#     print(commit_info)

#     # Print the commit information for each branch
#     for branch, info in commit_info.items():
#         print(f"Branch: {branch}")
#         print(f"  Commits:")
#         for user, commit_count in info['users'].items():
#             print(f"    {user}: {commit_count} commits")
#         print()




# ########### Pass as arguments

# import git
# import os, shutil, stat
# import argparse


# def remove_readonly(func, path, _):
#     os.chmod(path, stat.S_IWRITE)
#     func(path)

# def delete_directory(directory_path):
#     try:
#         # Set up the callback function to handle read-only files
#         shutil.rmtree(directory_path, onerror=remove_readonly)
#         print(f"Successfully deleted the directory: {directory_path}")
#     except Exception as e:
#         print(f"Error deleting the directory: {e}")

# def count_commits(remote_url, filter_branches):
#     repo = git.Repo.clone_from(remote_url, "temp_repo") # Clone the repository

#     # Initialize a dictionary to store commit counts and users
#     commit_info = {}

#     # Iterate over branches
#     for remote_branch in repo.remote().refs:
#         branch_name = remote_branch.name.split("/")[-1]

#         # Check if the branch should be filtered
#         if branch_name not in filter_branches:
#             continue

#         # Check if the local branch already exists
#         if branch_name not in repo.heads:
#             repo.create_head(branch_name, remote_branch) # Create a new local branch for each remote branch

#         repo.git.checkout(branch_name) # Checkout the branch

#         commits = list(repo.iter_commits(branch_name))

#         # Initialize a dictionary for the current branch
#         branch_info = {'commits': len(commits), 'users': {}}

#         # Iterate over commits in the current branch
#         for commit in commits:
#             author = commit.author.email
#             if author not in branch_info['users']:
#                 branch_info['users'][author] = 1
#             else:
#                 branch_info['users'][author] += 1

#         # Store the branch information in the overall dictionary
#         commit_info[branch_name] = branch_info

#     # Close the repo
#     repo.close()

#     # Clean up the temporary repository
#     delete_directory("temp_repo")
#     # shutil.rmtree("temp_repo") # Use shutil.rmtree for cleanup

#     return commit_info

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Count commits for each branch in a remote Git repository.')
#     parser.add_argument('remote_url', type=str, help='The URL of the remote Git repository.')
#     parser.add_argument('filter_branches', metavar='branch', type=str, nargs='+', help='The branches to filter.')

#     args = parser.parse_args()
#     remote_url = args.remote_url
#     filter_branches = args.filter_branches

#     commit_info = count_commits(remote_url, filter_branches)

#     print(commit_info)
    
#     # Print the commit information for each branch
#     for branch, info in commit_info.items():
#         print(f"Branch: {branch}")
#         print(f" Commits:")
#         for user, commit_count in info['users'].items():
#             print(f"    {user}: {commit_count} commits")
#         print()



############### Count code in Commit


import git
import os
import shutil
import stat
import argparse
import difflib
import time


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def delete_directory(directory_path):
    try:
        # Set up the callback function to handle read-only files
        shutil.rmtree(directory_path, onerror=remove_readonly)
        print(f"Successfully deleted the directory: {directory_path}")
    except Exception as e:
        print(f"Error deleting the directory: {e}")

        # If deletion fails, attempt to close any open files and retry
        try:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, "r") as f:
                        pass  # Attempting to open the file and immediately close it
            time.sleep(1)  # Wait for a short time to allow file handles to be released
            shutil.rmtree(directory_path, onerror=remove_readonly)
            print(f"Successfully deleted the directory after closing files: {directory_path}")
        except Exception as e:
            print(f"Error deleting the directory after closing files: {e}")

def count_commits(remote_url, filter_branches):
    repo = git.Repo.clone_from(remote_url, "temp_repo") # Clone the repository

    # Initialize a dictionary to store commit counts and users
    commit_info = {}

    # Iterate over branches
    for remote_branch in repo.remote().refs:
        branch_name = remote_branch.name.split("/")[-1]

        # Check if the branch should be filtered
        if branch_name not in filter_branches:
            continue

        # Check if the local branch already exists
        if branch_name not in repo.heads:
            repo.create_head(branch_name, remote_branch) # Create a new local branch for each remote branch

        repo.git.checkout(branch_name) # Checkout the branch

        commits = list(repo.iter_commits(branch_name))
        # print(commits)
        # Initialize a dictionary for the current branch
        branch_info = {'commits': len(commits), 'users': {}}
        total_lines_changed = 0
        # Iterate over commits in the current branch
        for commit in commits:
            
            # if commit.parents:
            #     # print(commit.diff(commit.parents[0])[0])
            #     diff = repo.git.diff(commit.parents[0], commit, ignore_blank_lines=True)
            #     lines_changed = diff.count('\n')
            #     total_lines_changed += lines_changed
            #     print(lines_changed)
            author = commit.author.email
            if author not in branch_info['users']:
                # branch_info['users'][author] = {'commit_count': 1, 'lines_modified': commit.count()}
                branch_info['users'][author] = {'commit_count': 1, 'lines_modified': 0}
            else:
                branch_info['users'][author]['commit_count'] += 1
                # branch_info['users'][author]['lines_modified'] += commit.count()
            
            # print(commit.tree)
            # print(commit.diff()[0])
            
            # try:
            #     print(commit.parents[0])
            # except Exception as e:
            #     print(e)

            # diffs = repo.head.commit.diff(commit)
            # for d in diffs:
            #     print(d.a_mode)

            # Calculate lines modified for each commit
            # diff = commit.diff(commit.parents[0] if commit.parents else None)
            # try:
            #     print(diff[0])
            # except Exception as e:
            #     print(e)

            # if commit.parents:
            #     diff = repo.git.diff(commit.parents[0], commit, ignore_blank_lines=True)
            # lines_changed = diff.count('\n')
            # branch_info['users'][author]['lines_modified'] = lines_changed
            
            # counted = 0
            # for file_diff in diff:
            #     counted += file_diff.count('\n')
            #     # print(counted)
            #     # if file_diff.a_blob is not None and file_diff.b_blob is not None:
            #     #     a_lines = file_diff.a_blob.data_stream.read().decode('utf-8').splitlines()
            #     #     b_lines = file_diff.b_blob.data_stream.read().decode('utf-8').splitlines()
                    
            #     #     lines_modified = sum(1 for line in difflib.unified_diff(a_lines, b_lines))
            #     #     # print(lines_modified)
            #     branch_info['users'][author]['lines_modified'] = counted

        # Store the branch information in the overall dictionary
        commit_info[branch_name] = branch_info

    # Close the repo
    repo.close()

    # Clean up the temporary repository
    delete_directory("temp_repo")

    return commit_info

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Count commits for each branch in a remote Git repository.')
    parser.add_argument('remote_url', type=str, help='The URL of the remote Git repository.')
    parser.add_argument('filter_branches', metavar='branch', type=str, nargs='+', help='The branches to filter.')

    args = parser.parse_args()
    remote_url = args.remote_url
    filter_branches = args.filter_branches

    commit_info = count_commits(remote_url, filter_branches)

    # print(commit_info)
    
    # Print the commit information for each branch
    for branch, info in commit_info.items():
        print(f"Branch: {branch}")
        print(f" Commits:")
        for user, data in info['users'].items():
            print(f"    {user}: {data['commit_count']} commits, {data['lines_modified']} lines modified")
        print()


# python test2.py https://gitlab.com/Codistan/artificial-intelligence/automationofmymarket main test staging