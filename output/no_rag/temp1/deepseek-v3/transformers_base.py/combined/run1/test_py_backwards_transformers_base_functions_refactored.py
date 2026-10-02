import pytest
import base as base_module
import typed_ast._ast3 as ast3_module

def test_base_node_transformer_initialization_with_none_context():
    # Setup: create a None context to pass to the transformer
    context = None

    # Execute: instantiate BaseNodeTransformer with the None context
    transformer = base_module.BaseNodeTransformer(context)

    # Assertion: the transformer should be created successfully
    # (no exception raised during initialization)

def test_visit_import_from_uses_name_replacement_when_no_module_rewrite_matches():
    # Setup: build an ImportFrom node (e.g. "from x import y").
    # The BaseImportRewrite visitor is constructed with an empty set of
    # rewrites (an ast.MatMult stand-in is passed in), so no module-level
    # rewrite matches and the visitor must fall through to name replacement.
    import_from_visitor = base_module.BaseImportRewrite(ast3_module.MatMult())

    source_module_node = import_from_visitor
    imported_symbol_node = ast3_module.MatMult()
    exported_symbol_node = import_from_visitor
    import_from_node = ast3_module.ImportFrom(
        *[source_module_node, imported_symbol_node, exported_symbol_node]
    )

    # Execution: dispatch the visit_ImportFrom visitor method on the node.
    result = import_from_visitor.visit_ImportFrom(import_from_node)

    # Assertion: the visitor processes the ImportFrom node without error
    # (exercising the branch that computes names to replace when no
    # module-level rewrite matches).
    assert result is None

def test_visit_import_from_with_no_rewrite_and_non_string_name_falls_through():
    # Setup: create a BaseImportRewrite with no rewrite rules configured
    NO_REWRITE = None
    base_import_rewrite = base_module.BaseImportRewrite(NO_REWRITE)

    # Setup: build an ImportFrom node with a MatMult in the names list
    # and no module specified, which shouldn't match any rewrite rule
    names = [NO_REWRITE, ast3_module.MatMult()]
    keywords = {}
    import_from_node = ast3_module.ImportFrom(*names, **keywords)

    # Execution: visiting the ImportFrom node should fall through to generic_visit
    # since there is no matching rewrite and no names to replace
    result = base_import_rewrite.visit_ImportFrom(import_from_node)

    # Assertion: the node is returned unchanged (generic_visit result)
    assert result is import_from_node

def test_visit_importfrom_with_unmatched_module_performs_no_rewrite():
    # Setup: construct a BaseImportRewrite and an ImportFrom node whose module
    # does not match any configured rewrite, to exercise the no-op fallthrough path.
    original_module_name = "\\x0bQHzaZ?\\tpM/wFtV"
    alternate_string = "%WE}A)"
    unmatched_module_names = {
        original_module_name: alternate_string,
        alternate_string: alternate_string,
    }
    import_rewriter = base_module.BaseImportRewrite(original_module_name)
    import_from_node = ast3_module.ImportFrom(
        module=original_module_name,
        names=[ast3_module.alias(name=alternate_string, asname=None)],
        level=0,
    )

    # Execution: visiting the ImportFrom node should not raise and should simply
    # delegate to generic_visit when no module rewrite matches.
    result = import_rewriter.visit_ImportFrom(import_from_node)

    # Assertion: the original node is returned unchanged since no rewrite applies.
    assert result is import_from_node

def test_visit_import_from_returns_same_node_when_module_not_in_rewrite_map():
    # Setup: create an ImportFrom node with a module name that is not in the rewrite map.
    # The dictionary is built with duplicate keys intentionally to mirror the original
    # state; the effective kwargs passed to ImportFrom are {'module': '\x0bQbHzaZ?\tpM/wFtV',
    # 'name': ''}.
    module_name_without_match = "\x0bQbHzaZ?\tpM/wFtV"
    empty_name = ""
    import_from_kwargs = {
        module_name_without_match: module_name_without_match,
        empty_name: module_name_without_match,
        module_name_without_match: module_name_without_match,
        empty_name: module_name_without_match,
        module_name_without_match: module_name_without_match,
    }
    import_from_node = ast3_module.ImportFrom(*import_from_kwargs, **import_from_kwargs)

    # create the rewriter with the ImportFrom node as context
    import_rewriter = base_module.BaseImportRewrite(import_from_node)

    # Execution: exercise the visitor method directly
    result_node = import_rewriter.visit_ImportFrom(import_from_node)

    # Assertion: without a matching rewrite, the visitor delegates to generic_visit,
    # which should return the same ImportFrom node.
    assert result_node is import_from_node

