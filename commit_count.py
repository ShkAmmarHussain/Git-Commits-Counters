""" Count Commits by users in each branch of a Repo """
import os
import git
import stat
import shutil

def remove_readonly(func, path, _):
    """" Change file to editable """
    os.chmod(path, stat.S_IWRITE)
    func(path)

def delete_directory(directory_path):
    """ Delete Cloned Repo """
    try:
        # Set up the callback function to handle read-only files
        shutil.rmtree(directory_path, onerror=remove_readonly)
        print(f"Successfully deleted the directory: {directory_path}")
    except Exception as e:
        print(f"Error deleting the directory: {e}")


def count_commits(remote_url):
    """ Counting Commits """
    repo = git.Repo.clone_from(remote_url, "temp_repo_2")  # Clone the repository

    # Initialize a dictionary to store commit counts and users
    commit_info = {}

    # Iterate over all branches
    for remote_branch in repo.remote().refs:
        branch_name = remote_branch.name.split("/")[-1]

        # Create a new local branch for each remote branch
        repo.create_head(branch_name, remote_branch)

        repo.git.checkout(branch_name)  # Checkout the branch

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
    delete_directory("temp_repo_2")

    return commit_info

### Uncomment Below to test the script

# if __name__ == "__main__":

#     remote_url = "Past Link of Repo here"  # Replace with your repository URL

#     commit_info = count_commits(remote_url)


#     # Print the commit information for each branch
#     for branch, info in commit_info.items():
#         print(f"Branch: {branch}")
#         print(f"  Commits:")
#         for user, commit_count in info['users'].items():
#             print(f"    {user}: {commit_count} commits")
#         print()
