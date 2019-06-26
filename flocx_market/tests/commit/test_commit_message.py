# pylint: disable=missing-docstring,redefined-outer-name,no-self-use,invalid-name

import os
import re
import subprocess

import git
import pytest

RE_PARSE_NAME = re.compile(r'(?P<name>.*) <(?P<email>[^>]+)> '
                           r'(?P<timestamp>\d+) (?P<tz>[-\d]+)')


@pytest.fixture
def commit_id():
    '''A dummy fixture that will be parameterized by the pytest_generate_tests
    function.'''


@pytest.fixture
def repo():
    '''Return a git.Repo object for the current directory'''
    return git.Repo('.')


@pytest.fixture
def commit(repo, commit_id):
    '''Convert the parametrized commit_id into a Commit object'''
    return repo.commit(commit_id)


@pytest.fixture
def max_subject_length():
    return int(os.environ.get('COMMIT_MAX_SUBJECT_LENGTH', 60))


def get_commits_from_pr():
    commit_range = os.environ.get('TRAVIS_COMMIT_RANGE')
    out = subprocess.check_output(['git', 'rev-list', commit_range])
    out = out.decode('utf-8')
    commits = out.splitlines()

    return commits


def pytest_generate_tests(metafunc):
    '''Get list of commits involved in current pull request'''

    if os.environ.get('TRAVIS_PULL_REQUEST', 'false') != 'false':
        commits = get_commits_from_pr()
    elif 'TRAVIS_COMMIT' in os.environ:
        commits = [os.environ.get('TRAVIS_COMMIT')]
    else:
        commits = ['HEAD']

    metafunc.parametrize('commit_id', commits)


def test_commit_subject_and_body(commit):
    '''Verify that a commit has a subject and body separated by a blank line'''
    message = commit.message.splitlines()
    assert len(message) > 2, (
        'Commit message must include both subject and body')

    assert not message[1], (
        'Commit message must have a blank line after the subject')


def test_commit_subject_no_period(commit):
    '''Verify that a commit message does not end with a "."'''
    subject = commit.message.splitlines()[0]
    assert not subject.endswith('.'), (
        'Commit messages should not end with a period (".")')


def test_commit_subject_length(commit, max_subject_length):
    '''Verify the length of the commit subject

    This will fail if the subject is longer than
    COMMIT_MAX_SUBJECT_LENGTH, if defined, otherwise
    60 characters.'''
    subject = commit.message.splitlines()[0]
    assert len(subject) < max_subject_length, (
        'Commit subject should be descriptive but less than '
        '{} characters'.format(max_subject_length))


def test_commit_has_reference(commit):
    '''Verify that a commit includes a bug/issue/task/etc reference'''
    has_gh_issue_refs = re.findall(r'#\d+', commit.message)
    has_taiga_issue_refs = re.findall(r'TG-\d+', commit.message)

    assert has_gh_issue_refs or has_taiga_issue_refs, (
        'Commit message does not reference related issue/task/user story. '
        'Use TG-nn to reference a Taiga task/story, or #nnn to reference a '
        'GitHub issue.'
    )
