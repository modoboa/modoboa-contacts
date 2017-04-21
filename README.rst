Address book plugin for Modoboa
===============================

|travis| |codecov|

Installation
------------

Install this extension system-wide or inside a virtual environment by
running the following command::

  $ pip install modoboa-contacts

Edit the settings.py file of your modoboa instance and apply the following modifications:

- add ``modoboa_contacts`` inside the ``MODOBOA_APPS`` variable like this::

    MODOBOA_APPS = (
        'modoboa',
        'modoboa.core',
        'modoboa.lib',
        'modoboa.admin',
        'modoboa.relaydomains',
        'modoboa.limits',
        'modoboa.parameters',
        # Extensions here
        # ...
        'modoboa_contacts',
    )

- Add the following at the begining of the file::

    from modoboa_contacts.settings import *

- Add ``webpack_loader`` to the ``INSTALLED_APPS`` variable

- Add the following lines::

    WEBPACK_LOADER = {
        'CONTACTS': {
            'CACHE': not DEBUG,
            'BUNDLE_DIR_NAME': 'modoboa_contacts/',
            'STATS_FILE': CONTACTS_STATS_FILES.get("dev" if DEBUG else "prod"),
            'IGNORE': ['.+\.hot-update.js', '.+\.map']
        }
    }

Finally, run the following commands to setup the database tables::

  $ cd <modoboa_instance_dir>
  $ python manage.py migrate
  $ python manage.py collectstatic
  $ python manage.py load_initial_data

For developpers
---------------

The frontend part of this plugin is developed with `VueJS 2 <https://vuejs.org/>`_ and
requires `nodejs <https://nodejs.org/en/>`_ and `webpack <https://webpack.js.org/>`_.

Once nodejs is installed on your system, run the following commands::

  $ cd frontend
  $ npm install
  $ npm run dev

To update dist files (the ones that will be distributed with the plugin), run::

  $ npm run build

.. |travis| image:: https://travis-ci.org/modoboa/modoboa-contacts.svg?branch=master
    :target: https://travis-ci.org/modoboa/modoboa-contacts

.. |codecov| image:: https://codecov.io/gh/modoboa/modoboa-contacts/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/modoboa/modoboa-contacts
