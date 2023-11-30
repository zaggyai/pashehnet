# pashehnet
Sensor network simulator publishing to MQTT broker

## Installation

If available from a package repository:
```bash
pip install pashehnet
```

Direct install from the repo:
```bash
pip install git+ssh://git@github.com/zaggyai/pashehnet
```

## Contributing

First, clone the repo!  :)

Make sure your virtual env is up-to-date:
```bash
pip install --upgrade pip wheel setuptools
```

Install package in dev/editable mode:
```bash
pip install -e .
```

Install dev environment dependencies such as `pytest`, `flake8` and supporting deps for tests:
```bash
pip install -r dev-requirements.py3
```

### Environment

You will need to define some environment variables for MQTT credentials that **_do not_** get checked into the repo:

- `MQTT_HOST` optional, defaults to `localhost`
- `MQTT_PORT` optional, defaults to `1883`
- `MQTT_USER`
- `MQTT_PWD`
- `MQTT_USE_SSL` optional, defaults to `false`

We like the cross-platform [direnv](https://direnv.net/) tool, but you do you!  :upside_down_face:

### Opening a Pull Request (PR)

Pull requests are a git workflow for managing branch merges with reviews and tests.  You can read more about them in the [GitHub docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).  Before opening a PR please make sure the following commands complete without errors in your local dev environment:

```bash
# Run linter
flake8 src/ tests/

# Run all unit tests
# Note we disable deprecation warnings for the time being;
# there's a method to the madness
pytest -W ignore::DeprecationWarning
```

Push your branch up to the `origin` setting the "upstream" flag in whatever tool you're using.  This sets the upstream association for any future push/pull attempts automatically and keeps your branch linked to the one on the `origin` server.  Example from the command line using the `-u` flag:

```bash
git push -u origin my-branch-name
```

After pushing your branch to GitHub, you can create a new PR either from the GitHub repo page or the link provided when you pushed the branch (some git tools provide this, some don't, ymmv).  When you create a PR please do the following:

1. Provide a brief one-line description of your branch work in the PR title
2. Provide a more detailed description if necessary in the description field; more common in bug fixes than new features unless there is something that reviewers might need to know to properly review your PR.  
3. Reference the GitHub issue in the description if this PR is related to one (e.g. something like `Closes #42` to reference work being done for issue 42).
4. Assign at least one other person to review.  They are only expected to review the code, not merge it.
5. Assign yourself to the PR as the party responsible for the PR
6. Set the project to `PashehNet`
7. Set the milestone to whatever the active milestone is
8. When the review is done and all checks have passed, please perform a "squash merge" to essentially roll all the commits in this branch into a single commit.  This makes the repo log a lot cleaner for maintenance.
9. Delete your branch.  This is also to keep the repo clean and reduce confusion re active work on the project.
10. Bask in the glory and our eternal appreciation for contributing to the project! 🙏
