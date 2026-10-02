import pytest

import journaling as journaling_module

def test_read_journal_entries_returns_iterable():
    """Verify that ReadJournalEntries can be called and returns an iterable of journal entries."""
    # Arrange
    READ_JOURNAL_ENTRIES = journaling_module.ReadJournalEntries

    # Act
    journal_entries = READ_JOURNAL_ENTRIES()

    # Assert
    assert journal_entries is not None, "ReadJournalEntries returned None"
    assert hasattr(journal_entries, "__iter__"), "ReadJournalEntries should return an iterable of entries"

def test_validate_raises_type_error_when_debits_and_credits_are_none():
    # Purpose:
    # Verify that JournalEntry.validate() raises a TypeError when debits and credits
    # are set to None (i.e., not iterable). The validation implementation attempts
    # to iterate over debits and credits to sum amounts, so passing None should fail.
    
    # Constants / Test data
    NONE_VALUE = None

    # Setup: construct a JournalEntry with None for debits, credits, and any other field
    journal_entry = journaling_module.JournalEntry(NONE_VALUE, NONE_VALUE, NONE_VALUE)

    # Execution & Assertion: calling validate should raise a TypeError because
    # the method tries to iterate over None for debits/credits.
    with pytest.raises(TypeError):
        journal_entry.validate()

