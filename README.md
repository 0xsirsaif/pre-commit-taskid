# pre-commit-taskid

A pre-commit hook that automatically appends task IDs from branch names to commit messages.

## Overview

This pre-commit hook extracts task IDs from your branch names and automatically appends them to your commit messages. It's designed to work with branch naming conventions like:

- `feature-1234`
- `bugfix-5678`
- `hotfix-9012`

When you make a commit, the hook will extract the numeric ID (e.g., `1234`) from your branch name and append it to your commit message in the format `#1234`.

## Installation

### Prerequisites

- Python 3.8 or higher
- [pre-commit](https://pre-commit.com/) package installed

### Using pip

```bash
pip install pre-commit-taskid
```

### From Source

```bash
git clone https://github.com/yourusername/pre-commit-taskid.git
cd pre-commit-taskid
pip install -e .
```

## Usage

1. Add the hook to your `.pre-commit-config.yaml` file:

```yaml
repos:
  - repo: https://github.com/yourusername/pre-commit-taskid
    rev: v0.1.0 # Use the specific version tag
    hooks:
      - id: taskid-prepender
```

2. Install the pre-commit hooks:

```bash
pre-commit install --hook-type prepare-commit-msg
```

3. Make commits as usual. The hook will automatically append the task ID to your commit messages.

## Examples

### Branch Name: `feature-1234`

Original commit message:

```
Add new login functionality
```

Modified commit message:

```
Add new login functionality #1234
```

### Branch Name: `bugfix-5678`

Original commit message:

```
Fix null pointer exception in user service
```

Modified commit message:

```
Fix null pointer exception in user service #5678
```

## Error Handling

- If no task ID is found in the branch name, the hook will log a warning but allow the commit to proceed without modification.
- If there are any errors during execution, the hook will log the error and exit with a non-zero status code.

## Configuration

No additional configuration is required. The hook will work out of the box with branch names that follow the format `branchName-{taskID}`.

## Development

### Testing

This project uses pytest for testing. The tests are organized into unit tests and integration tests.

#### Running Tests

You can run the tests using the provided script:

```bash
# Run all tests
run-taskid-tests

# Or using pytest directly
pytest

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Generate coverage report
pytest --cov=pre_commit_taskid --cov-report=term-missing
```

#### Test Structure

- **Unit Tests**: Test individual functions in isolation
- **Integration Tests**: Test the hook in a real Git repository

### Development Setup

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/pre-commit-taskid.git
cd pre-commit-taskid

# Install the package in development mode with dev dependencies
pip install -e ".[dev]"
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
