from functools import wraps
import os
import re
import subprocess

import git
import pytest


@pytest.fixture
def commit_id():
    '''A dummy fixture that will be parameterized by the pytest_generate_tests
    function.'''


@pytest.fixture
def repo():
    '''Return a git.Repo object for the current directory'''
    return git.Repo('.')


@pytest.fixture
def commit_message(repo, commit_id, commit_message_file):
    '''Return the commit message to be checked.

    If --message-from-file was specified on the command line, read the
    commit message from the named file. Otherwise, use the `git` module to
    resolve the named commit into a commit object and return the associated
    message.'''

    if commit_id == '__file__':
        with open(commit_message_file) as fd:
            message = '\n'.join(
                line.strip() for line in fd.readlines()
                if not line.startswith('#')
            )
            return message
    else:
        return repo.commit(commit_id).message


@pytest.fixture
def max_subject_length():
    '''Allow the maximum subject length to be configured in the environment.

    People somtimes have opinions on this sort of thing, so allow this
    value to be configured via an environment variable rather than
    requiring changes to the code.'''
    return int(os.environ.get('COMMIT_MAX_SUBJECT_LENGTH', 60))


def get_commits_from_pr():
    '''Generate list of commits to check from TRAVIS_COMMIT_RANGE.

    This uses `git rev-list` to resolve the given commit range into
    a list of commits.'''
    commit_range = os.environ.get('TRAVIS_COMMIT_RANGE')
    out = subprocess.check_output(['git', 'rev-list', commit_range])
    out = out.decode('utf-8')
    commits = out.splitlines()

    return commits


def pytest_generate_tests(metafunc):
    '''Get list of commits involved in current pull request'''

    commit_message_file = metafunc.config.getoption('--message-from-file')

    if commit_message_file:
        commits = ['__file__']
    elif os.environ.get('TRAVIS_PULL_REQUEST', 'false') != 'false':
        commits = get_commits_from_pr()
    elif 'TRAVIS_COMMIT' in os.environ:
        commits = [os.environ.get('TRAVIS_COMMIT')]
    else:
        commits = ['HEAD']

    metafunc.parametrize('commit_message_file', [commit_message_file])
    metafunc.parametrize('commit_id', commits)


def skip_if_fixup(func):
    '''A decorator to skip tests for fixup commits.

    A fixup commit (e.g., one generated with `git commit --fixup ...`) will
    not pass the commit checks. This decorator will skip tests using
    pytest.skip() if the commit being tested appears to be a fixup commit.
    '''

    @wraps(func)
    def wrapper(commit_message, *args, **kwargs):
        if commit_message.startswith('fixup!'):
            pytest.skip('skipping commit checks for fixup commit')

        return func(commit_message, *args, **kwargs)

    return wrapper


@skip_if_fixup
def test_commit_subject_and_body(commit_message):
    '''Verify that a commit has a subject and body separated by a blank line'''
    message = commit_message.splitlines()
    assert len(message) > 2, (
        'Commit message must include both subject and body')

    assert not message[1], (
        'Commit message must have a blank line after the subject')


@skip_if_fixup
def test_commit_subject_no_period(commit_message):
    '''Verify that a commit message does not end with a "."'''
    subject = commit_message.splitlines()[0]
    assert not subject.endswith('.'), (
        'Commit messages should not end with a period (".")')


@skip_if_fixup
def test_commit_subject_length(commit_message, max_subject_length):
    '''Verify the length of the commit subject

    This will fail if the subject is longer than
    COMMIT_MAX_SUBJECT_LENGTH, if defined, otherwise
    60 characters.'''
    subject = commit_message.splitlines()[0]
    assert len(subject) < max_subject_length, (
        'Commit subject should be descriptive but less than '
        '{} characters'.format(max_subject_length))


@skip_if_fixup
def test_commit_line_length(commit_message):
    '''Verify the length of the commit subject

    This will fail if lines in the message are not
    wrapped to < 75 characters.'''
    message = commit_message.splitlines()

    if len(message) > 2:
        for line in message[2:]:
            assert len(line) < 75, (
                'Commit message body should be wrapped at 75 characters')


@skip_if_fixup
def test_commit_has_reference(commit_message):
    '''Verify that a commit includes a bug/issue/task/etc reference'''
    has_gh_issue_refs = re.findall(r'#\d+', commit_message)
    has_taiga_issue_refs = re.findall(r'TG-\d+', commit_message)

    assert has_gh_issue_refs or has_taiga_issue_refs, (
        'Commit message does not reference related issue/task/user story. '
        'Use TG-nn to reference a Taiga task/story, or #nnn to reference a '
        'GitHub issue.'
    )


def test_commit_not_fixup(commit_message, request):
    if not request.config.option.block_fixups:
        pytest.skip('Use --block-fixups to block fixup commits')

    assert not commit_message.startswith('fixup!')
