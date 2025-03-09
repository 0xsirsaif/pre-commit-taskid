"""
Pytest configuration file for shared fixtures.
"""
import os
import tempfile
import subprocess
import shutil
import pytest


@pytest.fixture
def temp_git_repo():
    """
    Create a temporary Git repository for testing.
    
    This fixture creates a temporary directory, initializes a Git repository,
    configures Git user, and creates a sample file with an initial commit.
    
    Yields:
        tuple: A tuple containing (temp_dir, old_cwd) where temp_dir is the path
               to the temporary directory and old_cwd is the original working directory.
    """
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    old_cwd = os.getcwd()
    os.chdir(temp_dir)
    
    # Initialize a Git repository
    subprocess.run(["git", "init"], check=True, capture_output=True)
    
    # Configure Git user
    subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], check=True, capture_output=True)
    
    # Create a sample file and commit it
    with open("sample.txt", "w") as f:
        f.write("Sample content")
    
    subprocess.run(["git", "add", "sample.txt"], check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], check=True, capture_output=True)
    
    # Yield control back to the test
    yield temp_dir, old_cwd
    
    # Teardown: Clean up the temporary directory
    os.chdir(old_cwd)
    shutil.rmtree(temp_dir)


@pytest.fixture
def feature_branch_with_task_id(temp_git_repo):
    """
    Create a feature branch with a task ID.
    
    This fixture depends on the temp_git_repo fixture and creates a feature branch
    with a task ID, modifies the sample file, and stages the changes.
    
    Args:
        temp_git_repo: The temp_git_repo fixture.
        
    Returns:
        tuple: A tuple containing (temp_dir, old_cwd, task_id) where temp_dir is the path
               to the temporary directory, old_cwd is the original working directory,
               and task_id is the task ID in the branch name.
    """
    temp_dir, old_cwd = temp_git_repo
    task_id = "1234"
    
    # Create a feature branch with a task ID
    subprocess.run(["git", "checkout", "-b", f"feature-{task_id}"], check=True, capture_output=True)
    
    # Modify the sample file
    with open("sample.txt", "a") as f:
        f.write("\nAdditional content")
    
    subprocess.run(["git", "add", "sample.txt"], check=True, capture_output=True)
    
    return temp_dir, old_cwd, task_id 