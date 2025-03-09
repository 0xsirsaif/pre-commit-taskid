# pre-commit-taskid

A pre-commit hook that automatically appends task IDs from branch names to commit messages.

## Overview

This pre-commit hook extracts task IDs from your branch names and automatically appends them to your commit messages. It's designed to work with branch naming conventions like:

- `feature-1234`
- `bugfix-5678`
- `hotfix-9012`
- `user/feature-3456`
- `release/v1.0-7890`

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
git clone https://github.com/0xsirsaif/pre-commit-taskid.git
cd pre-commit-taskid
pip install -e .
```

## Usage

### 1. Add to your pre-commit config

Add the hook to your `.pre-commit-config.yaml` file:

```yaml
repos:
  - repo: https://github.com/0xsirsaif/pre-commit-taskid
    rev: v0.1.0 # Use the specific version tag
    hooks:
      - id: taskid-prepender
        stages: [prepare-commit-msg] # CRITICAL: This line is required!
```

### 2. Install the hook

```bash
# IMPORTANT: Must specify the prepare-commit-msg hook type
pre-commit install --hook-type prepare-commit-msg
```

### 3. Make commits as usual

The hook will automatically append the task ID to your commit messages.

## Examples

### Example 1: Feature Branch

```bash
# Create a feature branch
git checkout -b feature-1234

# Make changes and commit
git add .
git commit -m "Add login functionality"

# Resulting commit message:
# "Add login functionality (#1234)"
```

### Example 2: Bugfix Branch

```bash
# Create a bugfix branch
git checkout -b bugfix-5678

# Make changes and commit
git add .
git commit -m "Fix null pointer exception"

# Resulting commit message:
# "Fix null pointer exception (#5678)"
```

### Example 3: Branch with Path

```bash
# Create a branch with a path
git checkout -b user/feature-3456

# Make changes and commit
git add .
git commit -m "Add user profile"

# Resulting commit message:
# "Add user profile (#3456)"
```

## Troubleshooting

### Hook Not Running

If the hook isn't running:

1. Ensure you've installed it with the correct hook type:

   ```bash
   pre-commit install --hook-type prepare-commit-msg
   ```

2. Verify the hook is installed:

   ```bash
   ls -la .git/hooks/prepare-commit-msg
   ```

3. Check your `.pre-commit-config.yaml` includes `stages: [prepare-commit-msg]`

### Task ID Not Extracted

If the task ID isn't being extracted:

1. Ensure your branch name follows the pattern with a hyphen followed by numbers at the end:

   - ✅ `feature-1234`
   - ✅ `user/feature-1234`
   - ❌ `feature_1234`
   - ❌ `feature1234`

2. Check the branch name:

   ```bash
   git branch --show-current
   ```

### Parentheses Around Task ID

If you don't see parentheses around the task ID (e.g., `#(1234)` instead of `#1234`):

1. Update to the latest version of the package
2. Clean the pre-commit cache:
   ```bash
   pre-commit clean
   ```

## Advanced Configuration

### Using with Local Hooks

You can also use the hook locally without specifying a repository:

```yaml
repos:
  - repo: local
    hooks:
      - id: taskid-prepender
        name: Task ID Prepender
        entry: pre-commit-taskid
        language: python
        stages: [prepare-commit-msg]
        additional_dependencies: ["pre-commit-taskid==0.1.0"]
```

### Manual Testing

To test the hook manually:

```bash
# Create a test commit message
echo "Test commit" > .git/COMMIT_EDITMSG

# Run the hook manually
pre-commit-taskid .git/COMMIT_EDITMSG

# Check the result
cat .git/COMMIT_EDITMSG
```

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
git clone https://github.com/0xsirsaif/pre-commit-taskid.git
cd pre-commit-taskid

# Install the package in development mode with dev dependencies
pip install -e ".[dev]"
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
