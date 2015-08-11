#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et

import logging

# Third party libs
from git import Repo as _GitRepo
from git import refs as _GitRefs

from misc import Helper


class Repoindex(dict):
    """
    Maintains a list of repositories
    """

    def __init__(self):
        dict.__init__(self)

    def add_repo(self, deployment_name, repo_name, repo):
        """
        Add a repo to the index
        """
        if deployment_name not in self.keys():
            self[deployment_name] = {}
        if repo_name not in self[deployment_name].keys():
            self[deployment_name][repo_name] = self.verify_repo(repo)
        else:
            raise

    def verify_repo(self, repo):
        """
        Verify and correct the attributes of a repo object
        """
        if not repo.get('defaults').get('cache'):
            repo['defaults']['cache'] = 'common'
        return repo

    def sync_repos(self, sync_all=False):
        if sync_all:
            for deployment_name, repolist in Helper.sorted_dict(self).items():
                for repo_name, repo in Helper.sorted_dict(repolist).items():
                    for branch_name, branch_settings in Helper.sorted_dict(repo.get('branches')).items():
                        pass  # TODO
        else:
            pending_updates = []
            for deployment_name, repolist in Helper.sorted_dict(self).items():
                for repo_name, repo in Helper.sorted_dict(repolist).items():
                    if repo.get('updates').get('updated_refs'):
                        pending_updates.append(repo.get('updates'))
            if pending_updates:
                for pending_update in pending_updates:
                    cache_name = pending_update.get('cache').name

                    for updated_ref in pending_update.get('updated_refs'):
                        repo_name = updated_ref.get('repo')
                        repo_url = updated_ref.get('url')
                        repo_ref = updated_ref.get('ref')

                        for deployment_name, repolist in Helper.sorted_dict(self).items():
                            for repo_name, repo in Helper.sorted_dict(repolist).items():
                                for branch_name, branch_settings in Helper.sorted_dict(repo.get('branches')).items():
                                    if repo_url == branch_settings.get('url') and \
                                       repo_ref == branch_settings.get('ref') and \
                                       cache_name == branch_settings.get('cache', repo.get('defaults').get('cache')):
                                        repo.sync(branch_name, repo_ref, branch_settings.get('root', ''))