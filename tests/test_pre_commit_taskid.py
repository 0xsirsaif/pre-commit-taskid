import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock

from pre_commit_taskid import (
    extract_task_id,
    append_task_id_to_commit_msg,
    process_commit_msg,
    get_current_branch,
)


@pytest.mark.unit
class TestExtractTaskId:
    def test_extract_task_id_valid(self):
        """Test extracting task ID from valid branch names."""
        test_cases = [
            ("feature-1234", "1234"),
            ("bugfix-5678", "5678"),
            ("hotfix-9012", "9012"),
            ("user/feature-3456", "3456"),
            ("release/v1.0-7890", "7890"),
        ]
        
        for branch_name, expected_task_id in test_cases:
            assert extract_task_id(branch_name) == expected_task_id
    
    def test_extract_task_id_invalid(self):
        """Test extracting task ID from invalid branch names."""
        test_cases = [
            "master",
            "develop",
            "feature",
            "bugfix",
            "feature-abc",
            "feature_1234",
            "1234",
        ]
        
        for branch_name in test_cases:
            assert extract_task_id(branch_name) is None


@pytest.mark.unit
class TestAppendTaskIdToCommitMsg:
    def test_append_task_id_empty_message(self):
        """Test appending task ID to an empty commit message."""
        assert append_task_id_to_commit_msg("", "1234") == "#1234"
    
    def test_append_task_id_single_line(self):
        """Test appending task ID to a single-line commit message."""
        commit_msg = "Add new feature"
        expected = "Add new feature (#1234)"
        assert append_task_id_to_commit_msg(commit_msg, "1234") == expected
    
    def test_append_task_id_multi_line(self):
        """Test appending task ID to a multi-line commit message."""
        commit_msg = "Add new feature\n\nThis is a detailed description."
        expected = "Add new feature (#1234)\n\nThis is a detailed description."
        assert append_task_id_to_commit_msg(commit_msg, "1234") == expected
    
    def test_append_task_id_already_present(self):
        """Test appending task ID when it's already present in the commit message."""
        commit_msg = "Add new feature (#1234)"
        assert append_task_id_to_commit_msg(commit_msg, "1234") == commit_msg
        
        commit_msg = "Add new feature (#1234)\n\nThis is a detailed description."
        assert append_task_id_to_commit_msg(commit_msg, "1234") == commit_msg


@pytest.mark.unit
class TestProcessCommitMsg:
    @patch('pre_commit_taskid.get_current_branch')
    @patch('pre_commit_taskid.read_commit_msg_file')
    @patch('pre_commit_taskid.write_commit_msg_file')
    def test_process_commit_msg_success(self, mock_write, mock_read, mock_get_branch):
        """Test successful processing of commit message."""
        # Setup mocks
        mock_get_branch.return_value = "feature-1234"
        mock_read.return_value = "Add new feature"
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name
        
        try:
            # Call the function
            result = process_commit_msg(temp_file_path)
            
            # Assertions
            assert result == 0
            mock_get_branch.assert_called_once()
            mock_read.assert_called_once_with(temp_file_path)
            mock_write.assert_called_once_with(temp_file_path, "Add new feature (#1234)")
        finally:
            # Clean up
            os.unlink(temp_file_path)
    
    @patch('pre_commit_taskid.get_current_branch')
    def test_process_commit_msg_no_task_id(self, mock_get_branch):
        """Test processing commit message when no task ID is found."""
        # Setup mocks
        mock_get_branch.return_value = "master"
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name
        
        try:
            # Call the function
            result = process_commit_msg(temp_file_path)
            
            # Assertions
            assert result == 0  # Should return 0 even if no task ID is found
            mock_get_branch.assert_called_once()
        finally:
            # Clean up
            os.unlink(temp_file_path)
    
    @patch('pre_commit_taskid.get_current_branch')
    def test_process_commit_msg_exception(self, mock_get_branch):
        """Test processing commit message when an exception occurs."""
        # Setup mocks
        mock_get_branch.side_effect = Exception("Test exception")
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name
        
        try:
            # Call the function
            result = process_commit_msg(temp_file_path)
            
            # Assertions
            assert result == 1  # Should return 1 on exception
            mock_get_branch.assert_called_once()
        finally:
            # Clean up
            os.unlink(temp_file_path)


@pytest.mark.unit
class TestGetCurrentBranch:
    @patch('subprocess.run')
    def test_get_current_branch_success(self, mock_run):
        """Test successful retrieval of current branch."""
        # Setup mock
        mock_process = MagicMock()
        mock_process.stdout = "feature-1234\n"
        mock_run.return_value = mock_process
        
        # Call the function
        result = get_current_branch()
        
        # Assertions
        assert result == "feature-1234"
        mock_run.assert_called_once_with(
            ["git", "symbolic-ref", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
    
    @patch('subprocess.run')
    def test_get_current_branch_exception(self, mock_run):
        """Test exception handling when retrieving current branch."""
        # Setup mock
        mock_run.side_effect = Exception("Test exception")
        
        # Call the function and assert exception
        with pytest.raises(Exception):
            get_current_branch()
        
        # Assertions
        mock_run.assert_called_once() 