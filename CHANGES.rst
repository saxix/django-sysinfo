.. :changelog:

=======
History
=======

1.4 (7 Jan 2019)
-----------------
* add filtering to admin page
* fixes sections


1.3.2 (05 Jul 2018)
-----------------
* removes pip dependency


1.3.1 (23 Feb 2018)
-----------------
* add `extra` section to html output
* minor changes to html output


1.3 (10 Feb 2018)
-----------------
* add HTML info page
* Dropped support for old Django (<1.9) versions and Python 2.6
* Django 2.0 support has been added.


1.2 16 Aug 2017
---------------
* fixex python 3.6 compatibility
* new config '_ttl' to set cache max_age attribute


1.1 14 Jul 2017
---------------
* Django 1.11 compatibility
* handle broken database connections
* add new mail server informations
* new 'checks' API
* BACKWARD INCONPATIBLE: new config format


1.0 (15 Mar 2017)
-----------------
* fixes error in json serialization
* BACKWARD INCOMPATIBLE: by default all the sections are disabled
* allow both string and callable in extra section
* added new configuration parameters
* new management command

0.3 (27 Mar 2016)
-----------------
* dropped support Django<1.6
* add `settings.SYSINFO_USERS` to manage access
* default Basic Authentication protected urls
* removed 'sys' prefix from default urlpatterns
* new 'echo' endpoint

0.2 (13 Feb 2016)
-----------------
* add some infos
* output sorted to improve readibility
* add ability to filter sections (?s=os,python)
* add CACHES infos
* removed command line utility


0.1.1 (20 Jan 2016)
-------------------
* improved coverage
* fixes typos in copyright


0.1.0 (15 Jan 2015)
-------------------
* First release on PyPI.
