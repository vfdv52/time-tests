import pytest
from times import time_range, compute_overlap_time
import datetime

# First test: non-overlapping time ranges
def test_non_overlapping_time_ranges():
    """Test two time ranges that do not overlap"""
    range1 = time_range("2024-01-01 10:00:00", "2024-01-01 11:00:00")
    range2 = time_range("2024-01-01 12:00:00", "2024-01-01 13:00:00")
    
    result = compute_overlap_time(range1, range2)
    expected = []
    
    assert result == expected, f"Expected no overlap, but got {result}"

# Second test: Time range of multiple intervals
def test_multiple_intervals_both_ranges():
    """Test two time ranges that both contain several intervals each"""
    range1 = time_range("2024-01-01 10:00:00", "2024-01-01 11:00:00", 2, 0)
    range2 = time_range("2024-01-01 10:30:00", "2024-01-01 11:30:00", 3, 0)
    
    result = compute_overlap_time(range1, range2)
    
    # Should have overlaps between the intervals
    assert len(result) > 0, "Expected overlaps between multiple intervals"
    
    # Check that all overlaps are valid (start < end)
    for start, end in result:
        start_dt = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        assert start_dt < end_dt, f"Invalid overlap: {start} to {end}"

# Third test: adjacent time ranges
def test_adjacent_time_ranges():
    """Test two time ranges that end exactly when the other starts"""
    range1 = time_range("2024-01-01 10:00:00", "2024-01-01 11:00:00")
    range2 = time_range("2024-01-01 11:00:00", "2024-01-01 12:00:00")
    
    result = compute_overlap_time(range1, range2)
    
    # For adjacent ranges, there should be no actual overlap
    # since end1 == start2 means no shared time
    expected = []
    
    assert result == expected, f"Expected no overlap for adjacent ranges, but got {result}"

