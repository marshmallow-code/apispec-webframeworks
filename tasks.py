# -*- coding: utf-8 -*-
import os
import sys
import webbrowser

from invoke import task

docs_dir = 'docs'
build_dir = os.path.join(docs_dir, '_build')

@task
def test(ctx, watch=False, last_failing=False):
    """Run the tests.

    Note: --watch requires pytest-xdist to be installed.
    """
    import pytest
    syntax(ctx)
    args = []
    if watch:
        args.append('-f')
    if last_failing:
        args.append('--lf')
    args.append('apispec_webframeworks/tests')
    retcode = pytest.main(args)
    sys.exit(retcode)

@task
def syntax(ctx):
    """Run pre-commit hooks on codebase. Checks formatting and syntax."""
    ctx.run('pre-commit run --all-files --show-diff-on-failure', echo=True)

@task
def watch(ctx):
    """Run tests when a file changes. Requires pytest-xdist."""
    import pytest
    errcode = pytest.main(['-f'])
    sys.exit(errcode)

@task
def clean(ctx):
    ctx.run('rm -rf build')
    ctx.run('rm -rf dist')
    ctx.run('rm -rf apispec_webframeworks.egg-info')
    print('Cleaned up.')

@task
def readme(ctx, browse=False):
    ctx.run('rst2html.py README.rst > README.html')
    if browse:
        webbrowser.open_new_tab('README.html')
