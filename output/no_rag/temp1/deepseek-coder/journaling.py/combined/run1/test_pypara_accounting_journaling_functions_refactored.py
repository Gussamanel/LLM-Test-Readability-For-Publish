import pytest
import journaling as journaling

def test_reading_empty_journal_file_should_return_empty_list():
    # Given
    fake_path = "fake_path"
    journal_file_content = ""
    write_to_test_file(fake_path, journal_file_content)

    # When
    journaling.init(fake_path)

    # Then
    result = journaling.ReadJournalEntries()
    assert result == [], "Should return an empty list if no file exists"

def test_validate_journal_entry():
    # Setup
    NONE_TYPE = None
    JOURNAL_ENTRY = journaling.JournalEntry(NONE_TYPE, NONE_TYPE, NONE_TYPE)

    # Execution
    try:
        JOURNAL_ENTRY.validate()
    except AssertionError:
        # Assertion
        assert False, "An AssertionError was expected but was not raised"
    else:
        # Assertion
        assert True, "No AssertionError was raised but one was expected"

