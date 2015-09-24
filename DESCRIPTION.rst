Python package to fetch/download datasets via CKAN API.
=======================

This package will:
    1. fetch available datasets in London DataStore(http://data.london.gov.uk/) via CKAN API.
    2. break down the API response into:
        a) package_level(top level) data.
        b) resources_level data.
        c) tags_level data.
        d) groups_level data.
    3. utilize MySQL database as its backend storage. See the actual Schema design in data folder.
    4. periodically check for updates in order to:
        a) keep previous resources updated.
        b) fetch/download new resources.
