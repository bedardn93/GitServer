from git import Repo, rmtree
import os
import time

class GitServer():

    def __init__(self):
        self.repo = Repo.init()
        self.default_branch = None
        #self.git = self.repo.git
        #self.default_branch = self.repo.head.ref.name

    def clone(self, url, repo_name):
        self.repo = Repo.init()
        self.repo = self.repo.clone_from(url, repo_name)
        self.repo.config_reader()
        self.repo.config_writer()
        self.default_branch = self.repo.head.ref.name

    def add_branch(self, branch_name):
        self.repo.git.checkout(b=branch_name)

    def remove_branch(self, branch_name):
        if branch_name == self.default_branch:
            print(f"Can't remove default branch: {self.default_branch}")
        else:
            self.repo.git.checkout(self.default_branch)
            self.repo.delete_head(branch_name, force=True)

    def update_branch(self, branch_name):
        self.repo.git.checkout(branch_name)
        self.repo.git.pull('origin', branch_name)
        self.repo.git.checkout(self.default_branch)

    def test_add_file(self):
        open('test/klasdf', 'wb').close()
        self.repo.index.add(['klasdf'])
        self.repo.index.commit('asdlfasdfas')

    def merge_branch(self, branch_name):
        self.repo.git.checkout(branch_name)
        self.repo.git.pull('origin', branch_name)
        self.repo.git.checkout(self.default_branch)

def remove_repo(repo_name):
    rmtree(repo_name)

if __name__ == '__main__':
    try:
        repo_name = 'test'
        branch_name = 'test_branch'
        url = 'https://github.com/bedardn93/gitTestRepo.git'
        git_server = GitServer()
        git_server.clone(url, repo_name)
        git_server.add_branch(branch_name)
        git_server.test_add_file()
        git_server.update_branch(branch_name)
        git_server.remove_branch(branch_name)
    except Exception as e:
        print("***failed***")
        print(e)
    finally:
        git_server.repo.close()
        remove_repo(repo_name)