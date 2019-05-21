kismet_rest
===========

Python wrapper for Kismet REST interface.

.. image:: https://readthedocs.org/projects/kismet-rest/badge/?version=latest
  :target: https://kismet-rest.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status


Installing from PyPI
----------------------

::

    pip install kismet_rest


Installing from source
----------------------

::

    git clone https://github.com/kismetwireless/python-kismet-rest
    cd python-kismet-rest && pip install .


Usage examples
--------------


Legacy functionality (KismetConnector):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


::

    import kismet_rest
    conn = kismet_rest.KismetConnector(username="my_user", password="my_pass")
    for device in conn.device_summary():
        pprint.pprint(device)


Alerts since 2019-01-01:
~~~~~~~~~~~~~~~~~~~~~~~~

::

    import kismet_rest
    alerts = kismet_rest.Alerts()
    for alert in alerts.all(ts_sec=1546300800):
        print(alert)


Devices last observed since 2019-01-01:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    import kismet_rest
    devices = kismet_rest.Devices()
    for device in devices.all(ts=1546300800):
        print(device)


Developer notes:
----------------

* Formatting commit messages:
  * Correctly-formatted commit messages will be organized in CHANGELOG.rst
  * Commit messages are formatted like this ``type: audience: message !tag``
  * Type is for the type of change (``new``, ``chg``)
  * Audience is for the audience of the commit note(``usr``,``test``,``doc``)
  * The message part is pretty self-explanatory.
  * The optional tag allows you to flag a commit for exclusion from
  CHANGELOG.rst.(``minor`` or ``wip``)
  * A commit message like this: ``new: usr: Made a new widget.`` will appear in
  CHANGELOG.rst, under the appropriate release, under the "New" section.
  * More info on message formatting: https://github.com/vaab/gitchangelog
* Updating CHANGELOG.rst:
  * Install gitchangelog: ``pip3 install gitchangelog``
  * Make sure that ``__version__`` is correct in ``kismet_rest/__init__.py``
  * Build the new changelog: ``gitchangelog > CHANGELOG.rst``
