# GitHub Actions Automated Testing & CI Pipeline

<!-- Replace OWNER and REPOSITORY after creating the GitHub repository. -->
[![CI](https://github.com/OWNER/REPOSITORY/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/OWNER/REPOSITORY/actions/workflows/test.yml)

A beginner-friendly Python 3.12 project that demonstrates unit testing, Ruff linting, dependency caching, GitHub Actions, Conventional Commits, and merge protection.

## What this project demonstrates

- A small Python application with six utility functions and a runnable CLI example.
- Twelve Pytest unit tests for successful, invalid, and edge-case inputs.
- Ruff linting with a non-zero exit code when a rule is violated.
- A GitHub Actions workflow that runs on pushes and pull requests targeting `main`.
- Python 3.12 setup and pip dependency caching keyed from `requirements-dev.txt`.
- A repeatable PowerShell demo that observes an intentional test failure, corrects it, and verifies the test passes.
- Branch protection guidance for requiring both CI checks before merge.

## Project structure

```text
github-actions-testing-ci-pipeline/
├── .github/
│   └── workflows/
│       └── test.yml
├── app/
│   ├── __init__.py
│   ├── __main__.py
│   └── utils.py
├── scripts/
│   └── demo_failure.ps1
├── tests/
│   └── test_utils.py
├── .gitignore
├── LICENSE
├── pyproject.toml
├── README.md
├── requirements-dev.txt
└── requirements.txt
```

## Application architecture

`app/utils.py` contains the pure functions under test: whitespace normalization, word counting, palindrome detection, averaging, safe division, and Celsius-to-Fahrenheit conversion. `app/__main__.py` calls these functions to print a short demonstration when the package is run as a module. `tests/test_utils.py` checks each behavior, including empty inputs, a zero denominator, punctuation-only text, and the `-40 °C` conversion boundary.

The application uses only the Python standard library. `requirements.txt` is intentionally empty of runtime packages; `requirements-dev.txt` installs the test and lint tools with exact direct versions.

## Requirements

- Python 3.12
- Git
- PowerShell 7 or Windows PowerShell 5.1

## Install and run on Windows PowerShell

From the project folder:

```powershell
py -3.12 --version
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

If PowerShell blocks environment activation, either enable locally created scripts for your Windows account with `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`, or call `\.venv\Scripts\python.exe` directly instead of activating the environment.

Run the sample application:

```powershell
python -m app
```

Run the same quality checks as CI:

```powershell
python -m ruff check app tests
python -m pytest
```

Both commands return exit code `0` when their checks pass. Ruff and Pytest return a non-zero code when they find lint violations or test failures, so GitHub Actions marks the corresponding job as failed.

## Tests and recorded local results

The test suite includes positive cases, invalid inputs that must raise exceptions, and edge cases such as blank text and `-40 °C`. Run it from the project root with:

```powershell
python -m pytest
```

Execution log from the local Python 3.14 environment (the project and CI target Python 3.12):

```text
python -m ruff check app tests
All checks passed!
Exit code: 0

python -m pytest
12 passed
Exit code: 0
```

These are local command results. The GitHub Actions badge displays the remote workflow state after this folder is pushed to GitHub and the badge URL is updated.

## Intentional failure and resolution

Run the included PowerShell script to reproduce the complete cycle:

```powershell
.\scripts\demo_failure.ps1
```

The script temporarily creates a test with an incorrect expected value (`safe_divide(8, 2) == 5`). Pytest reports one failed test and exits non-zero. The script then corrects the expectation to `4`, reruns the test successfully, and removes the temporary test file. The intentionally failing test is not part of the committed suite, so it cannot break normal CI runs.

Recorded demonstration output:

```text
Step 1: run a test with an intentionally incorrect expected value.
1 failed
Expected result observed: pytest exited with code 1.
Step 2: correct the expected value and rerun the test.
1 passed
Resolution confirmed: pytest exited with code 0.
```

To demonstrate the same red-to-green result on GitHub, create a feature branch, temporarily change one expected value in a test, push it, and open a pull request to `main`. Confirm that `Tests / Pytest` fails. Correct the expectation, push again, and confirm both `Lint / Ruff` and `Tests / Pytest` pass before merging. Do not merge the intentionally failing revision.

## GitHub Actions workflow

Workflow file: `.github/workflows/test.yml`.

| Job check | What it does |
| --- | --- |
| `Lint / Ruff` | Installs the pinned development tools and runs `python -m ruff check app tests`. |
| `Tests / Pytest` | Installs the same dependencies and runs `python -m pytest`. |

Both jobs use `ubuntu-latest`, check out the source, and set up Python `3.12`. `actions/setup-python` uses `cache: pip` and `cache-dependency-path: requirements-dev.txt`, so changes to the development dependencies create a new pip cache key. The jobs are independent, so a lint failure does not hide the test result. The workflow grants only `contents: read` to the GitHub token.

## Create the GitHub repository and publish a pull request

Create an empty GitHub repository named `github-actions-testing-ci-pipeline` (do not pre-create a README, license, or `.gitignore`). In PowerShell, update the path and `OWNER` below to your actual values:

```powershell
cd "C:\Users\Admin\OneDrive\Desktop\mani\resume1 project\github-actions-testing-ci-pipeline"
git remote add origin https://github.com/OWNER/github-actions-testing-ci-pipeline.git
git push -u origin main
```

Update the two `OWNER/REPOSITORY` references at the top of this README with the actual repository owner and name; commit and push that edit so the status badge points to this workflow.

To make a feature branch and open a pull request with GitHub CLI:

```powershell
git switch -c feature/update-example
# Make and review your changes.
git add app tests README.md
git commit -m "feat: update example utility behavior"
git push -u origin feature/update-example
gh pr create --base main --head feature/update-example --title "feat: update example utility behavior" --body "Explain the change and its test coverage."
```

Use Conventional Commit subjects such as `feat:`, `fix:`, `test:`, `docs:`, and `ci:`. GitHub CLI authentication can be set up with `gh auth login` if needed.

## Require successful checks before merging

After the first workflow run has created the check names:

1. Open the repository's **Settings → Branches → Add branch protection rule** (or create a ruleset targeting `main`).
2. Set the branch pattern to `main`.
3. Enable **Require a pull request before merging**.
4. Enable **Require status checks to pass before merging** and select both `Lint / Ruff` and `Tests / Pytest`.
5. Save the rule. Optionally require the branch to be up to date before merging.

GitHub repository administrators or users with suitable settings permission must apply this repository setting; it cannot be enforced by a workflow file alone. Once configured, failed or pending required checks prevent pull request merges.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
