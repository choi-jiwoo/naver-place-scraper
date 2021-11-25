.. naverplacescraper documentation master file, created by
   sphinx-quickstart on Thu Nov 25 19:25:12 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to naverplacescraper's documentation!
=============================================

**naverplacescraper** is a package that scrapes description data and review data of a store registered in `Naver Place <https://map.naver.com>`_.

**Installation**
----------------

To use **naverplacescraper**, first install it using pip:

.. code-block:: shell

   $ pip install naverplacescraper

**Quick Start**
---------------

Searching by name
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from naverplacescraper import Store

   store = Store('<store name>', location='제주')  # location defaults to '서울'
   description = store.get_description()
   reviews = store.get_reviews()  # defaults to 100 reviews.

Documentation
~~~~~~~~~~~~~

The documentation is built with `Sphinx <https://www.sphinx-doc.org/en/master/index.html>`_.

.. toctree::
   :hidden:

   naverplacescraper

**License**
-----------

Licensed under the MIT License

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
