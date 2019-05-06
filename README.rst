kismet_rest
===========

Python wrapper for Kismet REST interface.


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
_______________________________________


::

    import kismet_rest
    conn = kismet_rest.KismetConnector(username="my_user", password="my_pass")
    for device in conn.device_summary():
        pprint.pprint(device)


Alerts since 2019-01-01:
________________________

::

    import kismet_rest
    alerts = kismet_rest.Alerts()
    for alert in alerts.yield_all(ts_sec=1546300800):
        print(alert)


Devices last observed since 2019-01-01:
_______________________________________

::

    import kismet_rest
    devices = kismet_rest.Devices()
    for device in devices.yield_all(ts=1546300800):
        print(device)
