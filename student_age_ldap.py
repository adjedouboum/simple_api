#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask import g, session, redirect, url_for
from flask_simpleldap import LDAP
import json
import os

app = Flask(__name__)
app.debug = True

if os.environ['LDAP_OPENLDAP'] is not None :
  app.config['LDAP_OPENLDAP'] = os.environ['LDAP_OPENLDAP']
else:
  app.config['LDAP_OPENLDAP'] = True

if os.environ['LDAP_OBJECTS_DN'] is not None :
  app.config['LDAP_OBJECTS_DN'] = os.environ['LDAP_OBJECTS_DN']
else:
  app.config['LDAP_OBJECTS_DN'] = 'dn'

if os.environ['LDAP_REALM_NAME'] is not None :
  app.config['LDAP_REALM_NAME'] = os.environ['LDAP_REALM_NAME']
else:
  app.config['LDAP_REALM_NAME'] = 'OpenLDAP Authentication'

if os.environ['LDAP_HOST'] is not None :
  app.config['LDAP_HOST'] = os.environ['LDAP_HOST']
else:
  app.config['LDAP_HOST'] = 'openldap.example.org'

if os.environ['LDAP_BASE_DN'] is not None :
  app.config['LDAP_BASE_DN'] = os.environ['LDAP_BASE_DN']
else:
  app.config['LDAP_BASE_DN'] = 'dc=users,dc=openldap,dc=org'

if os.environ['LDAP_USERNAME'] is not None :
  app.config['LDAP_USERNAME'] = os.environ['LDAP_USERNAME']
else:
  app.config['LDAP_USERNAME'] = 'cn=user,ou=servauth-users,dc=users,dc=openldap,dc=org'

if os.environ['LDAP_PASSWORD'] is not None :
  app.config['LDAP_PASSWORD'] = os.environ['LDAP_PASSWORD']
else:
  app.config['LDAP_PASSWORD'] = 'password'


app.config['LDAP_USER_OBJECT_FILTER'] = '(&(objectclass=inetOrgPerson)(uid=%s))'

ldap = LDAP(app)

# We retrieve student age file

if os.environ['student_age_file_path'] is not None :
  student_age_file_path  = os.environ['student_age_file_path']
else:
  student_age_file_path  = '/data/student_age.json'

student_age_file = open(student_age_file_path, "r")
student_age = json.load(student_age_file)

@app.route('/pozos/api/v1.0/get_student_ages', methods=['GET'])
@ldap.basic_auth_required
def get_student_ages():
    return jsonify({'student_ages': student_age })

@app.route('/pozos/api/v1.0/get_student_ages/<student_name>', methods=['GET'])
@ldap.basic_auth_required
def get_student_age(student_name): 
    if student_name not in student_age :
        abort(404)
    if student_name in student_age :
      age = student_age[student_name]
      del student_age[student_name]
      with open(student_age_file_path, 'w') as student_age_file:
        json.dump(student_age, student_age_file, indent=4, ensure_ascii=False)
    return age
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
