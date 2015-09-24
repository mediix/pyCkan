import json
import urllib2
from extras import byteify

ckan_packagelist_url='http://data.london.gov.uk/api/3/action/package_list'
ckan_package_url='http://data.london.gov.uk/api/3/action/package_show?id='
default = 'n/a'

def fetch():
    """
    """
    response = urllib2.urlopen(ckan_packagelist_url)
    assert response.code == 200

    packages_list = byteify(json.loads(response.read())['result'])

    for package in packages_list:
        r = urllib2.urlopen(ckan_package_url + package)
        assert r.code == 200
        response_dict = json.loads(r.read())
        assert response_dict['success'] is True
        api_result = byteify(response_dict['result'])
