import requests
import os
import re
from subprocess import call


JENKINS_URL = 'http://jenkins:8080'
USERNAME    = os.environ['JENKINS_USERNAME'].strip()
PASSWORD    = os.environ['JENKINS_PASSWORD'].strip()

# access login page
jar = requests.cookies.RequestsCookieJar()
ses = requests.Session()
r = ses.get(f'{JENKINS_URL}/login', cookies=jar)

# login
data = {'j_username': USERNAME, 'j_password': PASSWORD, 'from': '', 'Submit': 'Sign+in'}
r = ses.post(f'{JENKINS_URL}/j_spring_security_check', data=data, cookies=jar)

# get crumb
def get_crumb():
    r = ses.get(f'{JENKINS_URL}/crumbIssuer/api/json')
    return r.json()['crumb']

TOKEN_NAME = 'jenkins-jobs-token'

# delete token
crumb = get_crumb()
headers = {'Jenkins-Crumb': crumb}
r = ses.get(f'{JENKINS_URL}/user/{USERNAME}/configure', headers=headers)
token_uuid = re.search('token-uuid-input.*value="(.*)"', r.text)
if token_uuid:
    data = {'tokenUuid': token_uuid.group(1)}
    url = f'{JENKINS_URL}/user/{USERNAME}/descriptorByName/jenkins.security.ApiTokenProperty/revoke'
    r = ses.post(url, data=data, cookies=jar)

# create token
crumb = get_crumb()
headers = {'Jenkins-Crumb': crumb}
data = {'newTokenName': TOKEN_NAME}
url = f'{JENKINS_URL}/user/{USERNAME}/descriptorByName/jenkins.security.ApiTokenProperty/generateNewToken'
r = ses.post(url, data=data, cookies=jar, headers=headers)

TOKEN = r.json()['data']['tokenValue']

# create jenkins_jobs.ini
content = f"""
[jenkins]
user={USERNAME}
password={TOKEN}
url={JENKINS_URL}
query_plugins_info=False
"""

# write jenkins_jobs.ini
file = open("/etc/jenkins_jobs/jenkins_jobs.ini", "w")
file.write(content)
file.close()

# create jobs in jenkins
jobs_path='/etc/jenkins_jobs'
call(['jenkins-jobs', 'delete-all'], cwd=jobs_path)
call(['jenkins-jobs', 'update', 'jobs'], cwd=jobs_path)

