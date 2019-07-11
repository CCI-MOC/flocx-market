def pytest_addoption(parser):
    '''This adds the --message-from-file option to our commit tests, which
    allows us to read the commit message from a file (as required for use
    as a git commit-msg hook).'''

    parser.addoption(
        '--message-from-file',
        action='store',
        help='Read commit message from named file'
    )

    parser.addoption(
        '--block-fixups',
        action='store_true',
        default=False,
        help='Block fixup commits',
    )
