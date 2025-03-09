"""
Integration tests for the pre-commit-taskid hook.
"""
import os
import subprocess
import pytest


@pytest.mark.integration
def test_manual_hook_execution(feature_branch_with_task_id):
    """Test manual execution of the pre-commit hook."""
    temp_dir, _, task_id = feature_branch_with_task_id
    
    # Create a commit message file
    commit_msg_file = os.path.join(temp_dir, ".git", "COMMIT_EDITMSG")
    with open(commit_msg_file, "w") as f:
        f.write("Update sample file")
    
    # Run the pre-commit hook manually
    # Note: In a real scenario, this would be run by the pre-commit framework
    # Here we're simulating it by running the module directly
    result = subprocess.run(
        ["python", "-c", "from pre_commit_taskid import main; import sys; sys.argv = ['pre-commit-taskid', '{}'];"
                          "sys.exit(main())".format(commit_msg_file)],
        check=True,
        capture_output=True,
    )
    
    # Read the updated commit message
    with open(commit_msg_file, "r") as f:
        updated_msg = f.read()
    
    # Assert that the task ID was appended
    assert updated_msg == f"Update sample file #{task_id}"


# This test is commented out because it requires the pre-commit-taskid package to be installed
# and configured in the test environment. It's provided as an example of how to test the hook
# in a real Git repository with pre-commit installed.
"""
@pytest.mark.integration
@pytest.mark.skip(reason="Requires pre-commit-taskid to be installed")
def test_pre_commit_hook(temp_git_repo):
    temp_dir, old_cwd = temp_git_repo
    task_id = "1234"
    
    # Create a pre-commit config file
    pre_commit_config = '''
repos:
  - repo: local
    hooks:
      - id: taskid-prepender
        name: Task ID Prepender
        entry: pre-commit-taskid
        language: python
        stages: [prepare-commit-msg]
'''
    with open(".pre-commit-config.yaml", "w") as f:
        f.write(pre_commit_config)
    
    # Install pre-commit hooks
    subprocess.run(["pre-commit", "install", "--hook-type", "prepare-commit-msg"], check=True, capture_output=True)
    
    # Create a feature branch with a task ID
    subprocess.run(["git", "checkout", "-b", f"feature-{task_id}"], check=True, capture_output=True)
    
    # Modify the sample file
    with open("sample.txt", "a") as f:
        f.write("\nAdditional content")
    
    subprocess.run(["git", "add", "sample.txt"], check=True, capture_output=True)
    
    # Commit the changes
    result = subprocess.run(
        ["git", "commit", "-m", "Update sample file"],
        check=True,
        capture_output=True,
        text=True,
    )
    
    # Get the commit message
    commit_msg = subprocess.run(
        ["git", "log", "-1", "--pretty=%B"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    
    # Assert that the task ID was appended
    assert commit_msg == f"Update sample file #{task_id}"
"""


if __name__ == "__main__":
    pytest.main() 