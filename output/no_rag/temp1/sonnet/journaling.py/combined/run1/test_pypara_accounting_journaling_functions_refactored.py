import pytest
import journaling as journaling

def test_read_journal_entries_runs_without_error():
    # Test that ReadJournalEntries can be called without raising any exceptions
    # This verifies the basic functionality and initialization of the journal reading process
    
    # Execute the ReadJournalEntries function and verify it completes successfully
    journaling.ReadJournalEntries()

def test_journal_entry_validate_with_none_values():
    """
    Test that a JournalEntry can be created with None values for all fields
    and that validate() returns None when there are no debits or credits,
    since the total debit and credit amounts will both be zero (equal).
    """
    # Setup: Create a JournalEntry with None values for all fields
    NO_DATE = None
    NO_DEBITS = None
    NO_CREDITS = None

    journal_entry = journaling.JournalEntry(NO_DATE, NO_DEBITS, NO_CREDITS)

    # Execute: Validate the journal entry
    result = journal_entry.validate()

    # Assert: validate() should return None when debits and credits are balanced (both zero)
    assert result is None

