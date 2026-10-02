import pytest
import journaling as journaling

def test_read_journal_entries_initializes_without_error():
    # Test that ReadJournalEntries can be instantiated successfully
    # without raising any exceptions, verifying basic object creation works

    # Execute: Create an instance of ReadJournalEntries
    read_journal_entries = journaling.ReadJournalEntries()

    # Assert: Verify the instance was created successfully
    assert read_journal_entries is not None

def test_journal_entry_validate_with_none_values():
    """
    Test that a JournalEntry can be created with None values and that
    validate() returns None when there are no debits or credits,
    since the total debit and credit amounts will both be zero (equal).
    """
    # Setup: Define None values for JournalEntry fields (date, debits, credits)
    entry_date = None
    entry_debits = None
    entry_credits = None

    # Execution: Create a JournalEntry with None values and validate it
    journal_entry = journaling.JournalEntry(entry_date, entry_debits, entry_credits)
    validation_result = journal_entry.validate()

    # Assertion: Validate returns None when debits and credits are both empty/None (balanced)
    assert validation_result is None

