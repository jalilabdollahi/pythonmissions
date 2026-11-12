import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

import broken
from broken import (
    DuplicateFormat,
    Exporter,
    ExporterMeta,
    UnknownFormat,
    available,
    derive_format,
    export,
    get_exporter,
)


@pytest.fixture(autouse=True)
def isolated_registry(monkeypatch):
    monkeypatch.setattr(ExporterMeta, "registry", dict(ExporterMeta.registry))


def test_builtin_concrete_formats_are_registered():
    assert available() == ["csv", "jsonl", "psv", "tsv"]


def test_the_base_class_and_abstract_intermediates_are_not_registered():
    names = {cls.__name__ for cls in ExporterMeta.registry.values()}
    assert "Exporter" not in names, "the root interface is not a format"
    assert "DelimitedExporter" not in names, "abstract = True in the class body opts out"


def test_abstract_flag_is_not_inherited_by_concrete_subclasses():
    assert "tsv" in available(), "TsvExporter inherits from an abstract class but is concrete itself"
    assert export("tsv", [(1, "a"), (2, "b")]) == "1\ta\n2\tb"
    assert export("psv", [(1, "a")]) == "1|a"


def test_format_name_is_derived_from_class_name_or_taken_from_the_body():
    assert derive_format("CsvExporter") == "csv"
    assert derive_format("Exporter") == "exporter"
    assert derive_format("XmlWriter") == "xmlwriter"

    class XmlExporter(Exporter):
        abstract = False

    class FancyThing(Exporter):
        abstract = False
        format = "Fancy"

    assert XmlExporter.format == "xml" and "xml" in available()
    assert FancyThing.format == "fancy", "names are stored lowercase"


def test_subclass_does_not_inherit_its_parents_format_name():
    class CsvSemicolonExporter(broken.CsvExporter):
        def render_row(self, row):
            return ";".join(str(v) for v in row)

    assert CsvSemicolonExporter.format == "csvsemicolon"
    assert get_exporter("csv").__class__ is broken.CsvExporter
    assert export("csvsemicolon", [(1, 2)]) == "1;2"


def test_duplicate_format_names_are_rejected_at_class_creation():
    with pytest.raises(DuplicateFormat) as info:

        class AnotherCsvExporter(Exporter):
            abstract = False
            format = "CSV"

    assert "CsvExporter" in str(info.value)
    assert ExporterMeta.registry["csv"] is broken.CsvExporter, "the original registration is untouched"


def test_lookup_is_case_insensitive_and_unknown_names_list_alternatives():
    assert get_exporter("TSV").__class__.__name__ == "TsvExporter"
    with pytest.raises(UnknownFormat) as info:
        get_exporter("xlsx")
    assert "csv" in str(info.value) and "xlsx" in str(info.value)


def test_registry_is_shared_by_every_class_using_the_metaclass():
    class ParquetExporter(Exporter):
        abstract = False

        def render_row(self, row):
            return "|".join(map(str, row))

    assert get_exporter("parquet").export([(1, 2)]) == "1|2"
    assert ExporterMeta.registry is Exporter.registry
