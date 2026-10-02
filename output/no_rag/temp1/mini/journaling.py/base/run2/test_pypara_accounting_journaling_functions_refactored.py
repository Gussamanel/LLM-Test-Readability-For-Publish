import pytest

import journaling as journaling_module

def test_read_journal_entries_completes_and_returns_iterable_if_present():
    """
    Purpose:
    - Smoke test for journaling_module.ReadJournalEntries.
    - Verify the function executes without raising an exception.
    - If the function returns a value, ensure that value is iterable (e.g., list of entries).

    Structure:
    - Setup: None required for this basic call.
    - Execution: Call ReadJournalEntries and capture the result.
    - Assertion: Fail the test if an exception is raised. If a result is returned, assert it is iterable.
    """

    # Execution: call the function under test and capture the result
    try:
        journal_entries = journaling_module.ReadJournalEntries()
    except Exception as exc:
        # Assertion: the call should not raise; fail the test with the exception message if it does
        pytest.fail(f"ReadJournalEntries raised an unexpected exception: {exc}")

    # Assertion: if a value is returned, it should be iterable (e.g., list of journal entries)
    if journal_entries is not None:
        assert hasattr(journal_entries, "__iter__"), (
            "Expected ReadJournalEntries to return an iterable when a value is returned"
        )

def test_validate_passes_when_total_debits_equal_total_credits():
    # Purpose:
    # Verify that JournalEntry.validate() completes successfully (no AssertionError)
    # when total debits equal total credits. The validate() method returns None on success.

    # Constants / Test data setup
    EMPTY_DEBITS = []
    EMPTY_CREDITS = []
    METADATA = None  # placeholder for any additional data the JournalEntry constructor accepts

    # Setup: create a journal entry with equal totals (both zero)
    journal_entry = journaling_module.JournalEntry(EMPTY_DEBITS, EMPTY_CREDITS, METADATA)

    # Execution: call validate (should not raise)
    validation_result = journal_entry.validate()

    # Assertion: validate returns None on success and does not raise an AssertionError
    assert validation_result is None

