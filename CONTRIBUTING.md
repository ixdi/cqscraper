# Contributing

There are several strategies on how to contribute to a project on GitHub.

## Fork this repository

It is a better practice, possibly even enforced, that only pull requests from forks are accepted.

- Clone the main repository to your local machine:
- Add your fork as an upstream repository:

## Install for developers

Create a dedicated Python environment where to develop the project.

If you are using `pip`, follow something like

```sh
python -m venv venv
source venv/bin/activate
```

Install the package in `develop` mode.

```sh
pip install -e .
```

This configuration, together with the use of the `src` folder layer, guarantees that you will always run the code after installation.

## Make a new branch

From the `main` branch, create a new branch where to develop the new code.

**Note**: The `main` branch is from the main repository.

Develop the feature and keep regular pushes to your fork with comprehensible commit messages.

While you are developing, you can execute `pytest tests` as needed to run your unit tests.

## Update CHANGELOG

Update the changelog file under `CHANGELOG.md` with an explanatory bullet list of your contribution.
Add that list right after the main title and before the last version subtitle:

```
Changelog
=========

* here goes my new additions
* explain them shortly and well

vX.X.X (1900-01-01)
-------------------
```

Also, add your name to the authors list at `AUTHORS.md`.

## Pull Request

Once you have finished, you can create a pull request to the main repository and engage with the community.

**Before submitting a Pull Request, verify your development branch passes all tests. If you are developing new code, you should also implement new test cases.**
