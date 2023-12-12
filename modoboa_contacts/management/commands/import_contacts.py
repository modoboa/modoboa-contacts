"""Management command to import contacts from a CSV file."""

from django.core.management.base import BaseCommand, CommandError

from modoboa_contacts import models
from modoboa_contacts.importer import import_csv_file


class Command(BaseCommand):
    """Management command to import contacts."""

    help = "Import contacts from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--delimiter", type=str, default=",",
            help="Delimiter used in CSV file"
        )
        parser.add_argument(
            "email", type=str,
            help="Email address to import contacts for"
        )
        parser.add_argument(
            "file", type=str,
            help="Path of the CSV file to import"
        )

    def handle(self, *args, **options):
        addressbook = (
            models.AddressBook.objects.filter(
                user__email=options["email"]).first()
        )
        if not addressbook:
            raise CommandError(
                "Address Book for email '%s' not found" % options["email"]
            )
        try:
            import_csv_file(addressbook, options["file"], options["delimiter"])
        except RuntimeError as err:
            raise CommandError(err)
        self.stdout.write(
            self.style.SUCCESS("File was imported successfuly")
        )
