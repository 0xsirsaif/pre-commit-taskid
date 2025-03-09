import re
import sys
import subprocess
from typing import Optional, Tuple


def get_current_branch() -> str:
    """Get the name of the current Git branch.

    Returns:
        str: The current branch name.

    Raises:
        subprocess.CalledProcessError: If the git command fails.
    """
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting current branch: {e}", file=sys.stderr)
        raise


def extract_task_id(branch_name: str) -> Optional[str]:
    """Extract the task ID from a branch name.

    The branch name is expected to follow the format: branchName-{taskID}
    For example: feature-1234 or bugfix-5678

    Args:
        branch_name (str): The branch name to parse.

    Returns:
        Optional[str]: The extracted task ID, or None if no task ID was found.
    """
    # Match any pattern ending with a hyphen followed by numbers
    match = re.search(r'-(\d+)$', branch_name)
    if match:
        return match.group(1)
    return None


def read_commit_msg_file(commit_msg_file: str) -> str:
    """Read the commit message from the specified file.

    Args:
        commit_msg_file (str): Path to the commit message file.

    Returns:
        str: The commit message.
    """
    try:
        with open(commit_msg_file, 'r') as f:
            return f.read()
    except IOError as e:
        print(f"Error reading commit message file: {e}", file=sys.stderr)
        sys.exit(1)


def write_commit_msg_file(commit_msg_file: str, commit_msg: str) -> None:
    """Write the commit message to the specified file.

    Args:
        commit_msg_file (str): Path to the commit message file.
        commit_msg (str): The commit message to write.
    """
    try:
        with open(commit_msg_file, 'w') as f:
            f.write(commit_msg)
    except IOError as e:
        print(f"Error writing commit message file: {e}", file=sys.stderr)
        sys.exit(1)


def append_task_id_to_commit_msg(commit_msg: str, task_id: str) -> str:
    """Append the task ID to the commit message if it's not already present.

    Args:
        commit_msg (str): The original commit message.
        task_id (str): The task ID to append.

    Returns:
        str: The commit message with the task ID appended.
    """
    # Check if the task ID is already in the commit message
    if f"#{task_id}" in commit_msg:
        return commit_msg

    # Append the task ID to the first line of the commit message
    lines = commit_msg.splitlines()
    if not lines:
        return f"#{task_id}"

    lines[0] = f"{lines[0]} #{task_id}"
    return "\n".join(lines)


def process_commit_msg(commit_msg_file: str) -> int:
    """Process the commit message file to append the task ID.

    Args:
        commit_msg_file (str): Path to the commit message file.

    Returns:
        int: 0 for success, non-zero for failure.
    """
    try:
        # Get the current branch name
        branch_name = get_current_branch()
        
        # Extract the task ID from the branch name
        task_id = extract_task_id(branch_name)
        
        if not task_id:
            print(f"No task ID found in branch name: {branch_name}", file=sys.stderr)
            return 0  # Continue with commit even if no task ID is found
        
        # Read the commit message
        commit_msg = read_commit_msg_file(commit_msg_file)
        
        # Append the task ID to the commit message
        updated_msg = append_task_id_to_commit_msg(commit_msg, task_id)
        
        # Write the updated commit message
        write_commit_msg_file(commit_msg_file, updated_msg)
        
        print(f"Successfully appended task ID #{task_id} to commit message")
        return 0
    except Exception as e:
        print(f"Error processing commit message: {e}", file=sys.stderr)
        return 1


def main() -> int:
    """Main entry point for the pre-commit hook.

    Returns:
        int: 0 for success, non-zero for failure.
    """
    if len(sys.argv) != 2:
        print("Usage: pre-commit-taskid COMMIT_MSG_FILE", file=sys.stderr)
        return 1
    
    commit_msg_file = sys.argv[1]
    return process_commit_msg(commit_msg_file)


if __name__ == "__main__":
    sys.exit(main())
