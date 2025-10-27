import pytest
from times import time_range, compute_overlap_time


def test_given_input():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    result = compute_overlap_time(large, short)
    print(f"Overlap: {result}")


def test_no_overlap():
    """Test two time ranges that do not overlap at all"""
    range1 = time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00")
    range2 = time_range("2010-01-12 14:00:00", "2010-01-12 15:00:00")
    
    result = compute_overlap_time(range1, range2)
    
    # When there's no overlap, should return empty list
    assert result == []
    print(f"No overlap result: {result}")


def test_multiple_intervals_overlap():
    """Test two time ranges that both contain several intervals each"""
    # range1: split into 2 intervals with 30 second gaps
    range1 = time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00", 2, 30)
    
    # range2: split into 3 intervals with 60 second gaps
    range2 = time_range("2010-01-12 10:20:00", "2010-01-12 10:50:00", 3, 60)
    
    result = compute_overlap_time(range1, range2)
    
    # Should have 3 valid overlaps (some intervals don't overlap)
    assert len(result) == 3
    print(f"Multiple intervals overlap: {result}")
    
    # Verify all returned overlaps are valid (start <= end)
    for start, end in result:
        assert start <= end, f"Invalid overlap: {start} > {end}"


def test_adjacent_time_ranges():
    """Test two time ranges that end exactly at the same time when the other starts"""
    range1 = time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00")
    range2 = time_range("2010-01-12 11:00:00", "2010-01-12 12:00:00")
    
    result = compute_overlap_time(range1, range2)
    
    # Boundary point overlap where start == end
    assert result == [('2010-01-12 11:00:00', '2010-01-12 11:00:00')]
    print(f"Adjacent ranges result: {result}")


def test_backwards_time_range():
    """Test that a backwards time range (end before start) raises ValueError"""
    with pytest.raises(ValueError) as excinfo:
        time_range("2010-01-12 12:00:00", "2010-01-12 10:00:00")
    
    # Check that the error message is meaningful
    assert "End time" in str(excinfo.value)
    assert "must be after start time" in str(excinfo.value)
    print(f"Caught expected error: {excinfo.value}")