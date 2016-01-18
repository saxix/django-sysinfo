.. _installation:

Installation methods
====================

**Note:** It is recommended that you always use the latest release of django-sysinfo with the latest release of Django. If you are using an older version of Django, then please check out the :ref:`Compatible Django Versions <django-versions>` page for more information.

For information on configuring django-sysinfo, see the :ref:`getting started <index>` guide.


pip
---

You can install django-sysinfo into your system, or virtual environment, by running the following command in a terminal::

    $ pip install django-sysinfo


easy_install
------------

The popular easy_install utility can be used to install the latest django-sysinfo release from the Python Package Index. Simply run the following command in a terminal::

    $ sudo easy_install django-sysinfo


Git
---

Using Git to install django-sysinfo provides an easy way of upgrading your installation at a later date. Simply clone the `public git repository <http://github.com/etianen/django-sysinfo>`_ and symlink the ``src/sysinfo`` directory into your ``PYTHONPATH``::

    $ git clone git://github.com/etianen/django-sysinfo.git
    $ cd django-sysinfo.git
    $ git checkout release-1.9.3
    $ ln -s src/sysinfo /your/pythonpath/location/sysinfo
