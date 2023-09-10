import csv
import os

from github import Auth
from github import Github
from github import PaginatedList
from github import Repository

from const.constants import GITHUB_ACCESS_TOKEN, ATTRIBUTES


def search_repositories_by_language(
        g: Github,
        language: str,
        sort: str = 'stars',
        order: str = 'desc'
) -> PaginatedList.PaginatedList[Repository.Repository]:
    """
    Search repositories by language.
    :param g: an instance of GitHub
    :param language: the language to search for
    :param sort: the sort field (stars, forks, updated) - default: stars
    :param order: the sort order (asc, desc) - default: desc
    :return: a paginated list of repositories
    """
    return g.search_repositories(query=f"language:{language}", sort=sort, order=order)


def get_metadata_from_repository(
        repo: Repository.Repository,
) -> dict:
    """
    Get metadata from a repository.
    :param repo: a GitHub repository
    :return: a dictionary with the repository metadata
    """
    metadata = {}
    metadata['full_name'] = repo.full_name
    metadata['html_url'] = repo.html_url
    metadata['stargazers_count'] = repo.stargazers_count
    metadata['forks_count'] = repo.forks_count
    metadata['collaborators'] = repo.get_contributors().totalCount
    metadata['open_issues_count'] = repo.open_issues_count
    metadata['description'] = repo.description
    metadata['archived'] = repo.archived
    metadata['created_at'] = repo.created_at
    metadata['updated_at'] = repo.updated_at
    metadata['pushed_at'] = repo.pushed_at
    return metadata


def save_repositories_csv(
        repositories: PaginatedList.PaginatedList[Repository.Repository],
        total_repositories: int = 10,
        file_name: str = 'repositories.csv'):
    """
    Save repositories to a CSV file.
    :param repositories: the repositories paginated list from GitHub
    :param total_repositories: the total number of repositories to save
    :param file_name: file name to save the CSV
    :return: nothing
    """
    with open(f'output/{file_name}', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=ATTRIBUTES)
        writer.writeheader()
        for repo in repositories[:total_repositories]:
            repo_metadata = get_metadata_from_repository(repo)
            writer.writerow(repo_metadata)


if __name__ == '__main__':
    if GITHUB_ACCESS_TOKEN not in os.environ:
        raise Exception('GITHUB_ACCESS_TOKEN not found in environment variables.')
    auth = Auth.Token(os.environ[GITHUB_ACCESS_TOKEN])
    g = Github(auth=auth)
    go_repos = search_repositories_by_language(g, 'go')
    save_repositories_csv(go_repos, 100)