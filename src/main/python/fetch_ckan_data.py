# fetch data from packages
import MySQLdb
import urllib2
import json

con = MySQLdb.connect(user='mehdi', passwd='pashmak.mN2', db='research_uk_public_data', host='granweb01', charset="utf8", use_unicode=True)

ckan_packagelist_url='http://data.london.gov.uk/api/3/action/package_list'
ckan_package_url='http://data.london.gov.uk/api/3/action/package_show?id='
default = 'n/a'

#------------------------------------------------------------------------------
def table_exists(table_name=None, con=None):
  """"""
  cur = con.cursor()
  try:
    cur.execute("SHOW TABLES;")
  except MySQLdb.Error as e:
    print "ERROR FROM => table_exists %d: %s" % (e.args[0], e.args[1])
  finally:
    cur.close()

  table_names = cur.fetchall()
  table_names = [x[0].encode('utf-8') for x in table_names]
  exists = True if table_name in table_names else False
  return exists

def byteify(input):
  """
  input: JSON object
  returns: UTF-8 encoded json
  """
  from dateutil import parser
  import re
  def clean(inp):
    """"""
    delete = ""
    i = 1
    while (i < 0x20):
      delete += chr(i)
      i+=1
    inp = inp.translate(None, delete)
    inp = re.sub('<[^<]+?>', '', inp)
    return inp
  #
  parse_date = lambda x: parser.parse(x).strftime("%Y-%m-%d") if not x == '' else x
  if isinstance(input, dict):
    return { byteify(key): byteify(value) for key, value in input.iteritems() }
  elif isinstance(input, list):
    return [byteify(elem) for elem in input]
  elif isinstance(input, unicode):
    try:
      return parse_date(clean(input.encode('utf-8')))
    except:
      return clean(input.encode('utf-8').strip())
  else:
    return input

# def check_id(table_name=None, col_name=None, value=None, con=None):
#   """"""
#   cur = con.cursor()
#   try:
#     cur.execute("SELECT id FROM %(table_name)s WHERE %(col_name)s = '%(value)s';" % {'table_name':table_name, 'col_name':col_name, 'value':value})
#     db_response = cur.fetchone()
#   except MySQLdb.Error as e:
#     print "ERORR FROM => check_id %d: %s" % (e.args[0], e.args[1])
#   finally:
#     cur.close()

#   return db_response

def insert_package(data, table_name=None, con=None):
  """"""
  # Check if the ID exists in the db
  cur = con.cursor()
  _id = check_id(table_name, 'name', data['name'], con)
  if _id is None:
    cur.execute("SHOW COLUMNS FROM %(table_name)s;"% {'table_name':table_name})
    cols = cur.fetchall()
    cols = [x[0].encode('utf-8') for x in cols[1:-2]]
    col_names = ','.join('`%s`' % col for col in cols)
    wildcards = ','.join(['%s'] * len(cols))
    #Preparing data to be inserted
    item = tuple([check(data.get(col, default)) for col in cols])
    insert_sql = """INSERT INTO %s (%s,`birth`)
                    VALUES (%s,NOW())""" % (table_name, col_names, wildcards)
    try:
      cur.executemany(insert_sql, [item])
      con.commit()
      cur.execute("SELECT LAST_INSERT_ID();")
      db_response = cur.fetchone()
      _id = db_response[0]
    except MySQLdb.Error as e:
      print "ERROR FROM => insert_package %d: %s" % (e.args[0], e.args[1])
    finally:
      cur.close()

  return _id

def insert_resources(data, package_id, table_name=None, con=None):
  """"""
  cur = con.cursor()
  # _id = check_id(table_name, 'name', data[0]['name'], con)
  # if _id is None:
  cur.execute("SHOW COLUMNS FROM %(table_name)s;"% {'table_name':table_name})
  cols = cur.fetchall()
  cols = [x[0].encode('utf-8') for x in cols[2:-2]]
  col_names = ','.join('`%s`' % col for col in cols)
  wildcards = ','.join(['%s'] * len(cols))
  #Preparing data to be inserted
  item = [tuple([check(elem.get(col, default)) for col in cols]) for elem in data]
  insert_sql = """INSERT INTO %s (`package_id`,%s,`birth`)
                  VALUES (%s,%s,NOW())""" % (table_name, col_names, package_id, wildcards)
  try:
    cur.executemany(insert_sql, item)
    con.commit()
  except MySQLdb.Error as e:
    print "ERROR FROM => insert_resources %d: %s" % (e.args[0], e.args[1])
  finally:
    print "MESSAGE FROM => insert_resources: DATA INSERTED"
    cur.close()

def create_schema(data, table_name=None, con=None):
  """"""
  if table_exists(table_name, con) == False:
    ignore = ['id', 'lazyboy_json', 'datastore_json', 'cache_url', '  webstore_last_updated', 'csvlint_json', 'mimetype_inner', 'hash', ' revision_id', 'or_principal_investigator', 'or_resource_provider', 'owner_org', 'or_responsible_party_role', 'or_owner', 'or_processor', 'odi-certificate', 'or_point_of_contact', 'or_originator', 'or_distributor', 'dp_created', 'or_publisher', 'or_author', 'or_user', 'hash', 'mimetype', 'cache_url', 'cache_last_updated', 'dp_modified', 'temporal_coverage_to', 'temporal_coverage_from']
    column_types = []
    for column in data.keys():
      column_types.append((column, 'TEXT'))
    column_types = list(filter(lambda x: x[0] not in ignore, column_types))
    columns = ',\n'.join("`%s` %s" % x for x in column_types)
    if table_name == 'ckan_packages':
      template_table = """CREATE TABLE %(table_name)s (id INT(10) PRIMARY KEY   AUTO_INCREMENT NOT NULL, %(columns)s, birth DATETIME NOT NULL, time_stamp   TIMESTAMP);"""
    else:
      template_table = """CREATE TABLE %(table_name)s (id INT(10) PRIMARY KEY   AUTO_INCREMENT NOT NULL, package_id INT(10) NOT NULL , %(columns)s, birth DATETIME NOT NULL, time_stamp   TIMESTAMP);"""
    create = template_table % {'table_name':table_name, 'columns': columns}
    cur = con.cursor()
    try:
      cur.execute(create)
      con.commit()
    except MySQLdb.Error as e:
      print "MESSAGE FROM => create_schema %d: %s" % (e.args[0], e.args[1])
    finally:
      print "TABLE %s, CREATED" % table_name
      cur.close()
  else:
    print "TABLE %s EXISTS" % table_name

##-----------------------------------------------------------------------------
if __name__ == '__main__':
  #
  def check(inp):
    """"""
    if isinstance(inp, list):
      return [check(elem) for elem in inp]
    elif isinstance(inp, dict):
      return { check(k): check(v) for k, v in inp.iteritems() }
    elif isinstance(inp, str):
      return str(inp).strip() if inp is not None else ''
    elif inp is None:
      return ''
    else:
      return inp

  def flatten(structure, key='', path='', flattened=None):
    """"""
    if flattened is None:
      flattened = {}
    if not isinstance(structure, (dict, list)):
      flattened[((path + "_") if path else "") + key] = structure
    elif isinstance(structure, list):
      for i, item in enumerate(structure):
        flatten(item, "%d" % i, "".join(filter(None,[path,key])), flattened)
    else:
      for new_key, value in structure.items():
        flatten(value, new_key, "".join(filter(None,[path,key])), flattened)
    return flattened

  def check_id(table_name=None, con=None, *args):
    """"""
    print args, type(args), len(args)
    col = [ elem.keys() for elem in args ][0]
    val = [ tuple(elem.values()) for elem in args ]

    col = ', '.join('%s=%s AND' % c for c in col)

    print "COLUMNS: %s" % col
    print "VALUES: %s" % val

    sql = """SELECT id FROM %(table_name)s
             WHERE %(col_val)s;""" % {'table_name':table_name, 'col_val':col_val}
    try:
      cur = con.cursor()
      cur.execute(sql)
      db_response = cur.fetchone()
    except MySQLdb.Error as e:
      print "ERROR FROM => check_id %d: %s" % (e.args[0], e.args[1])


  response = urllib2.urlopen(ckan_packagelist_url)
  assert response.code == 200
  packages_list = byteify(json.loads(response.read())['result'])

  for package in packages_list[5:6]:
    r = urllib2.urlopen(ckan_package_url + package)
    assert r.code == 200
    response_dict = json.loads(r.read())
    assert response_dict['success'] is True
    api_result = byteify(response_dict['result'])

    #------------------------------------------------------
    # Insert package_level_data
    try:
      top_level = dict(filter(lambda (k, v): not isinstance(v, (dict, list)), api_result.items()))
      # create_schema(top_level, 'ckan_packages', con)
      # package_id = insert_package(check(top_level), 'ckan_packages', con)
    except(TypeError, KeyError, ValueError) as err:
      print "ERROR FROM => main", err

    #------------------------------------------------------
    # Insert resources_level_data
    resources_data = [flatten(check(elem)) for elem in api_result['resources']]
    # try:
    #   create_schema(resources_data[0], 'ckan_package_resources', con)
    #   insert_resources(resources_data, package_id, 'ckan_package_resources', con)
    # except (TypeError, KeyError, ValueError) as err:
    #   print "ERROR FROM => main", err

    #------------------------------------------------------
    # Insert tags_level_data
    tags_data = [flatten(check(elem)) for elem in api_result['tags']]
    # try:
    #   create_schema(tags_data[0], 'ckan_package_tags', con)
    #   insert_resources(tags_data, package_id, 'ckan_package_tags', con)
    # except (TypeError, KeyError, ValueError) as err:
    #   print "ERROR FROM => main", err

    #------------------------------------------------------
    # Insert groups_level_data
    groups_data = [flatten(check(elem)) for elem in api_result['groups']]
    # try:
    #   create_schema(groups_data[0], 'ckan_package_groups', con)
    #   insert_resources(groups_data, package_id, 'ckan_package_groups', con)
    # except (TypeError, KeyError, ValueError) as err:
    #   print "ERROR FROM => main", err
