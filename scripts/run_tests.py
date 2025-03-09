#!/usr/bin/env python3
"""
Script to run the tests for the pre-commit-taskid package.
"""
import os
import sys
import subprocess


def run_tests():
    """Run the tests for the pre-commit-taskid package."""
    # Get the root directory of the project
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Change to the root directory
    os.chdir(root_dir)
    
    # Use the current Python executable
    python_exe = sys.executable
    
    # Run the tests
    print("Running unit tests...")
    unit_result = subprocess.run(
        [python_exe, "-m", "pytest", "-m", "unit", "-v"],
        capture_output=True,
        text=True,
    )
    
    print(unit_result.stdout)
    if unit_result.stderr:
        print(f"Errors: {unit_result.stderr}")
    
    print("\nRunning integration tests...")
    integration_result = subprocess.run(
        [python_exe, "-m", "pytest", "-m", "integration", "-v"],
        capture_output=True,
        text=True,
    )
    
    print(integration_result.stdout)
    if integration_result.stderr:
        print(f"Errors: {integration_result.stderr}")
    
    # Run coverage report
    print("\nGenerating coverage report...")
    coverage_result = subprocess.run(
        [python_exe, "-m", "pytest"],  # Use the default options from pytest.ini
        capture_output=True,
        text=True,
    )
    
    print(coverage_result.stdout)
    if coverage_result.stderr:
        print(f"Errors: {coverage_result.stderr}")
    
    # Return success if all tests passed
    return unit_result.returncode == 0 and integration_result.returncode == 0


def main():
    """Main entry point."""
    success = run_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 