import os
import pytest
from src.collector import compute_hash

def test_compute_hash(tmp_path):
    # Create a test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello world")

    # Compute hash
    result = compute_hash(test_file)

    # Precomputed SHA256 for "hello world"
    expected = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    assert result == expected
