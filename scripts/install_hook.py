#!/usr/bin/env python3
"""
Script to install the pre-commit-taskid hook in a Git repository.
This script creates a pre-commit configuration file and installs the hook.
"""

import os
import subprocess
import sys
from pathlib import Path


def is_git_repo():
    """Check if the current directory is a Git repository."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def create_pre_commit_config():
    """Create a pre-commit configuration file if it doesn't exist."""
    config_path = Path(".pre-commit-config.yaml")
    
    if config_path.exists():
        print(f"Pre-commit config file already exists at {config_path}")
        
        # Check if our hook is already in the config
        with open(config_path, "r") as f:
            config_content = f.read()
        
        if "taskid-prepender" in config_content:
            print("The taskid-prepender hook is already configured.")
            return
        
        print("Adding taskid-prepender hook to existing config...")
        
        # Append our hook to the existing config
        with open(config_path, "a") as f:
            f.write("\n# Added by pre-commit-taskid install script\n")
            f.write("  - repo: local\n")
            f.write("    hooks:\n")
            f.write("      - id: taskid-prepender\n")
            f.write("        name: Task ID Prepender\n")
            f.write("        entry: pre-commit-taskid\n")
            f.write("        language: python\n")
            f.write("        stages: [prepare-commit-msg]\n")
    else:
        print(f"Creating pre-commit config file at {config_path}")
        
        # Create a new config file
        with open(config_path, "w") as f:
            f.write("repos:\n")
            f.write("  - repo: local\n")
            f.write("    hooks:\n")
            f.write("      - id: taskid-prepender\n")
            f.write("        name: Task ID Prepender\n")
            f.write("        entry: pre-commit-taskid\n")
            f.write("        language: python\n")
            f.write("        stages: [prepare-commit-msg]\n")


def install_pre_commit_hook():
    """Install the pre-commit hook."""
    try:
        subprocess.run(
            ["pre-commit", "install", "--hook-type", "prepare-commit-msg"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Pre-commit hook installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing pre-commit hook: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: pre-commit command not found.")
        print("Please install pre-commit using 'pip install pre-commit' and try again.")
        sys.exit(1)


def main():
    """Main function."""
    if not is_git_repo():
        print("Error: Not a Git repository.")
        print("Please run this script from within a Git repository.")
        sys.exit(1)
    
    create_pre_commit_config()
    install_pre_commit_hook()
    
    print("\nInstallation complete!")
    print("The pre-commit-taskid hook is now installed and will automatically")
    print("append task IDs from your branch names to your commit messages.")
    print("\nExample:")
    print("  Branch: feature-1234")
    print("  Commit message: 'Add new feature'")
    print("  Result: 'Add new feature #1234'")


if __name__ == "__main__":
    main() 