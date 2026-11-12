# Mission 279 - Exporter Registry Metaclass
# A metaclass that registers every concrete exporter by format name, but not abstract bases.


class DuplicateFormat(Exception):
    pass


class UnknownFormat(KeyError):
    pass


def derive_format(class_name):
    """CsvExporter -> csv, ParquetV2Exporter -> parquetv2."""
    name = class_name[: -len("Exporter")] if class_name.endswith("Exporter") else class_name
    return (name or class_name).lower()


class ExporterMeta(type):
    registry = {}

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if cls.abstract:
            return  # `abstract` is read from this class body only; it is not inherited
        key = cls.format or derive_format(name)
        key = key.lower()
        cls.format = key
        ExporterMeta.registry[key] = cls


class Exporter(metaclass=ExporterMeta):
    format = None
    abstract = False
    content_type = "text/plain"

    def render_row(self, row):
        raise NotImplementedError

    def export(self, rows):
        return "\n".join(self.render_row(r) for r in rows)


class CsvExporter(Exporter):
    content_type = "text/csv"

    def render_row(self, row):
        return ",".join(str(v) for v in row)


class JsonLinesExporter(Exporter):
    format = "jsonl"

    def render_row(self, row):
        return "[" + ", ".join(repr(v) for v in row) + "]"


class DelimitedExporter(Exporter):
    abstract = True
    separator = "\t"

    def render_row(self, row):
        return self.separator.join(str(v) for v in row)


class TsvExporter(DelimitedExporter):
    content_type = "text/tab-separated-values"


class PipeExporter(DelimitedExporter):
    format = "psv"
    separator = "|"


def get_exporter(name):
    try:
        return ExporterMeta.registry[name.lower()]()
    except KeyError:
        raise UnknownFormat(f"unknown format {name!r}; available: {available()}") from None


def available():
    return sorted(ExporterMeta.registry)


def export(name, rows):
    return get_exporter(name).export(rows)


if __name__ == "__main__":
    print(available())
    print(export("tsv", [(1, "a"), (2, "b")]))
