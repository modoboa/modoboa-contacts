import csv

from modoboa_contacts.importer.backends.outlook import OutlookBackend


BACKENDS = [
    OutlookBackend,
]


def detect_import_backend(fp, delimiter: str = ";"):
    reader = csv.DictReader(
        fp,
        delimiter=delimiter,
        skipinitialspace=True
    )
    columns = reader.fieldnames
    rows = reader

    for backend in BACKENDS:
        if backend.detect_from_columns(columns):
            return backend, rows

    raise RuntimeError("Failed to detect backend to use")


def import_csv_file(addressbook, csv_filename: str, delimiter: str):
    with open(csv_filename) as fp:
        backend, rows = detect_import_backend(fp, delimiter)
        backend(addressbook).proceed(rows)
