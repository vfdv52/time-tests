import datetime
import pytest
from times import time_range, compute_overlap_time


@pytest.mark.parametrize("time_range_1, time_range_2, expected", [
    # Test case 1: Basic overlap - large range contains smaller range
    pytest.param(
        ("2010-01-12 10:00:00", "2010-01-12 12:00:00", 1, 0),
        ("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60),
        [('2010-01-12 10:30:00', '2010-01-12 10:37:00'),
         ('2010-01-12 10:38:00', '2010-01-12 10:45:00')],
        id="basic_overlap"
    ),
    
    # Test case 2: Non-overlapping time ranges
    pytest.param(
        ("2024-01-01 10:00:00", "2024-01-01 11:00:00", 1, 0),
        ("2024-01-01 14:00:00", "2024-01-01 15:00:00", 1, 0),
        [],
        id="no_overlap"
    ),
    
    # Test case 3: Multiple intervals in both ranges
    pytest.param(
        ("2010-01-12 10:00:00", "2010-01-12 11:00:00", 2, 30),
        ("2010-01-12 10:20:00", "2010-01-12 10:50:00", 3, 60),
        3,  # Expected number of valid overlaps
        id="multiple_intervals"
    ),
    
    # Test case 4: Adjacent time ranges (boundary touch)
    pytest.param(
        ("2024-01-01 10:00:00", "2024-01-01 11:00:00", 1, 0),
        ("2024-01-01 11:00:00", "2024-01-01 12:00:00", 1, 0),
        [],
        id="adjacent_ranges"
    ),
])
def test_compute_overlap_time(time_range_1, time_range_2, expected):
    """Test compute_overlap_time with various time range scenarios"""
    # Generate time ranges
    range1 = time_range(*time_range_1)
    range2 = time_range(*time_range_2)
    
    # Compute overlap
    result = compute_overlap_time(range1, range2)
    
    # Check result based on expected type
    if isinstance(expected, list):
        # Exact match for specific expected overlaps
        assert result == expected, f"Expected {expected}, but got {result}"
    elif isinstance(expected, int):
        # Check count of valid overlaps (for multiple intervals case)
        assert len(result) == expected, f"Expected {expected} overlaps, but got {len(result)}"
        # Verify all overlaps are valid (start < end)
        for start, end in result:
            start_dt = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
            end_dt = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
            assert start_dt < end_dt, f"Invalid overlap: {start} > {end}"


def test_backwards_time_range():
    """Test that a backwards time range (end before start) raises ValueError"""
    start_time = "2010-01-12 10:15:00"
    end_time = "2010-01-12 10:00:00"
    
    with pytest.raises(ValueError, match="Start time must be before end time"):
        time_range(start_time, end_time)