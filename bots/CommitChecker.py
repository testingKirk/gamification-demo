import requests
from sys import argv
from database import MongoDB

def check_commits(owner, name, branch):
    print("checking commits:")
    url = f"https://api.github.com/repos/{name}/commits?sha={branch}"

    response = requests.get(url)
    if response.status_code == 200:
        commits = response.json()

        # extract authors of commits
        commit_authors = [commit['author']['login'] for commit in commits if commit['author'] is not None]

        # check if the user has committed to the branch
        if owner in commit_authors:
            print(f"The user {owner} has committed to the branch {branch}.")
            save_dict = dict()
            save_dict['_id'] = owner
            save_dict['commit'] = {
                'completed': True,
                'points': 10  # may want to do a entry that tracks total points for later
            }
            save_dict['user_data'] = {
                'xp': 10
            }
            db = MongoDB()
            db.dump_user_data(save_dict)
            user_data = db.read_user_data(save_dict)
            db.close_connection()
        else:
            print(f"The user {owner} has not committed to the branch {branch}.")
    else:
        print("Failed to fetch commits")


if __name__ == '__main__':
    repo_owner = argv[1]
    repo_name = argv[2]
    repo_branch = argv[3]

    check_commits(repo_owner, repo_name, repo_branch)