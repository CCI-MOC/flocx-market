import pytest


def pytest_addoption(parser):

    parser.addoption(
        '--message-from-file',
        action='store',
        help='Read commit message from named file'
    )
