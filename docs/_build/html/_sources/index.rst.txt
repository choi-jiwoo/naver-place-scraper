.. naverplacescraper documentation master file, created by
   sphinx-quickstart on Thu Nov 25 19:25:12 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to naverplacescraper's documentation!
=============================================

**naverplacescraper** is a package that scrapes description data and review data of a store registered in `Naver Place <https://map.naver.com>`_.

.. warning::

   The package only supports Korean language

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

Searching by ID
~~~~~~~~~~~~~~~

Search with the store ID registered in naver place.

.. code-block:: python

   from naverplacescraper import Store

   store = Store('<store ID>', location='제주', by_id=True)
   description = store.get_description()
   reviews = store.get_reviews()

For more example, see notebook `here <https://github.com/choi-jiwoo/naver-place-scraper/blob/master/example/naverplace.ipynb>`_.

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
