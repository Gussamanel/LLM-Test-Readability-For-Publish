import journaling as module_0

def test_case_0():
    # Prepare
    journal_entries = ['Entry 1', 'Entry 2', 'Entry 3']

    # Execute
    read_journal_entries = module_0.ReadJournalEntries()

    # Assert
    assert read_journal_entries == journal_entries

def test_validate_journal_entry():
    """
    This test case involves validating a journal entry. It's checking if the total debit
    matches the total credit in a balanced bookkeeping system. If the total debit and total 
    credit don't match, it'll raise an assertion error.
    """

    ### Setup
    NONE_TYPE = None
    JOURNAL_ENTRY = module_0.JournalEntry(NONE_TYPE, NONE_TYPE, NONE_TYPE)

    ### Execution 
    VALIDATED_JOURNAL_ENTRY = JOURNAL_ENTRY.validate()

    ### Assertion
    assert VALIDATED_JOURNAL_ENTRY is None, "Validated journal entry is not None"

    ### Additional assertion to check journal entry total debits and credits
    TOTAL_DEBIT = sum(i.amount for i in JOURNAL_ENTRY.debits)
    TOTAL_CREDIT = sum(i.amount for i in JOURNAL_ENTRY.credits)

    ### Compare debits and credits
    assert TOTAL_DEBIT == TOTAL_CREDIT, "Total Debits and Credits are not equal"

