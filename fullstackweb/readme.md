Full Stack Web Engineer Exercise
================================

Overview
--------

This exercise requires the engineer to perform a range of tasks that are typical in developing, deploying, and operating a live site. 

The project is a blank slate, the only artifact being the products.json file, which will form the basis for the application's data model.

The exit criteria of this exercise is to observe:

* What method and technology was used to deploy core infrastructure like databases, web servers, etc.
* What technologies were selected and why?
* What architecture patterns were selected and why?

The over arching goal of this exercise is to gain insight into how the engineer approaches building and deploying a full stack project. Given the limited time box of most of our explorations, a strong grasp of current tools and frameworks crucial to rapidly building prototypes capable of semi-production deployment is key.

Scenario
--------

This exercise is based on a simple end to end scenario; building a basic product viewer web application.

We have a raw product file, products.json, and the following requirements:

1. That a user can view the product images and titles through a web application
2. That an application developer can access the data through an API
3. That a user can search for a product by entering a keyword on the web application
4. That an operations person can view basic graphs on the load/use of the application

Requirements
------------

Your code should meet the following requirements:

* Be [PEP8] compliant
* Implement a unit test for each material function, capable of being tested using [pytest] or [nosetest]
* Contain sufficient docstrings and comments to make it easy to reason about


Things to keep in mind
----------------------
* Full stack encompasses everything from design, development, deployment and operations
* This is a mile wide, inch deep exercise, focus on clearing all tasks at the same level, and avoid going deeper than need be into any one task

Submission Process
------------------

To avoid dependencies on services like AWS, we suggest you complete your work inside a [Docker] container, using Ubuntu 13.04 (64 bit) or 13.10 (64 bit) as the base OS, and simply check-in your application's docker file as part of your overall Github fork.

Disclaimer
---------

Merchant product listings in data/products.json are the property of the respective merchant.

[PEP8]:http://legacy.python.org/dev/peps/pep-0008/
[pytest]:http://pytest.org/latest/
[nosetest]:https://nose.readthedocs.org/en/latest/
[Docker]:https://www.docker.io/

Rory's Solution Notes
=====================

Assumptions
-----------

* Based on the requirements, the solution needs to be Python based.  Python is not a language I have experience with, so that portion of the solution is likely sub-optimal.  However, the overall architecture and front-end should be solid.
* Building in Docker as per instructions, but this would not be recommended for a production application at this time due to the way Docker has to run with admin privileges leaving open the possibility that, if a vulnerability is found in Docker that allows code to break out of the sandbox, it would be executing as root on the host system.
* Installing all components in a single Docker container, although this is unlikely in practice.
* Pages are designed to statically render the page for the initial load, but to use a search API to grab all updates.  This is done to optimize for SEO, since search engines sometimes struggle to index dynamically loaded content, while simultaneously delivering the client a seamless experience free of page reloads.  The search API can be accessed at /product/?q=<your query>.  Additionally, as requested, there is a RESTful API that implements basic List and Details actions.  This API is exposed on a separate port, 8888, using the /product/ and /product/<id>/ semantics.
* Currently, items are sorted based on their price, but this is arbitrary.
* The client-side portion of the application is built using a framework I developed and have open sourced, Xintricity.js.  The framework is built on top of Backbone and jQuery
* I am not a designer

Software
--------
* Ubuntu 13.10 x64 running Docker – selected per recommended OSes, since an LTS version was not an option I figured I might as well go with the latest.
* Python 2.7 – Python selected per the requirements for PEP8 compliance and pytest-ability, went with 2.7 rather than the 3.X series because there is an officially supported Ubuntu package and because there are some number of packages that are still not compatible with 3.X and, prior to starting the exercise, I was not certain whether I might need these.
* Nginx + uWSGI – Chose nginx for its highly efficient design, ease of configuration, and substantial support base that ensures it will be maintainable for the foreseeable future.  While I have not tested this with Python, in other languages I have also found that using a process-per-worker model typically puts a huge premium on memory – often memory would be depleted while CPU was at 25-30% utilization.  Using a multi-threaded server in conjunction with nginx is typically much more efficient, since it reduces the overhead of loading all the shared libraries into memory for each process.
* Django - I selected the Django framework, as it is the leading Python web framework, provides a lot of auto-generated boilerplate functionality to get up and running faster, and has a large ecosystem of libraries.
* Primary data storage - while there was no explicit requirement, it seemed very foreseeable that this sort of product viewer will likely have sorting and/or filtering functionality on a couple different fields at some point in the future.  As such, a column/row based datastore is actually a natural fit for primary storage, and a traditional SQL DB actually works quite effectively for this purpose.  To scale this up, since the  application appears likely to be read heavy, replicas could easily be used and, should data size or write performance become an issue, a solution such as MySQL Cluster could be employed.  NoSQL datastores were also considered, particularly column based stores like HBase and Cassandra (since they would have better performance characteristics for filtering by column value than a document based store).  However, given the parameters outlined, there was no clear use-case necessitating a NoSQL solution as a primary storage mechanism.
* elasticsearch was selected to provide enhanced search functionality for its reliability, scalability and performance, as well as its schema-less design, which allows the models being indexed to evolve without requiring any updates to a static schema for search functionality.  While a simpler solution using existing components might have sufficed for a prototype (e.g. a text search against the DB or even a client-side search in javascript, given the limited number of items), neither of these would produce as good of results, scale as well, or generally be suitable for production use.

