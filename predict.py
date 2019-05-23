# Copyright 2019 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import urllib3, requests, json

# retrieve your wml_service_credentials_username, wml_service_credentials_password, and wml_service_credentials_url from the
# Service credentials associated with your IBM Cloud Watson Machine Learning Service instance

wml_instance = 'a7ea00ba-abd1-4516-838e-fe298495a427'
wml_deployment = '13cbddfd-69ad-4d1d-8234-a26f29d3f715'
wml_service_credentials_url = 'https://us-south.ml.cloud.ibm.com'
wml_service_credentials_username = '8b9b89e0-aaa5-4fcd-8a5d-b0d8c85c5152'
wml_service_credentials_password = '26de7ff9-7bb6-45ce-b311-d0b14061748f'
wml_service_api_key = 'SPUIW7odR8YWYSJ5ij_3PgzD77Z59K4A9GIJcnfwU_xb'

wml_credentials={
  "url": wml_service_credentials_url,
  "username": wml_service_credentials_username,
  "password": wml_service_credentials_password
}

headers = urllib3.util.make_headers(basic_auth='{username}:{password}'.format(username=wml_credentials['username'], password=wml_credentials['password']))
url = '{}/v3/identity/token'.format(wml_credentials['url'])
response = requests.get(url, headers=headers)
mltoken = json.loads(response.text).get('token')
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
array_of_values_to_be_scored = [93, 22, 163, 25, 49, 'F', 'N', 'N', 110]

payload_scoring = {"fields": ["AVGHEARTBEATSPERMIN", "PALPITATIONSPERDAY", "CHOLESTEROL", "BMI", "AGE", "SEX", "FAMILYHISTORY", "SMOKERLAST5YRS", "EXERCISEMINPERWEEK"], "values": [array_of_values_to_be_scored]}
scoring_url = '{url}/v3/wml_instances/{instance}/deployments/{deployment}/online'.format(url=wml_service_credentials_url, instance=wml_instance, deployment=wml_deployment)
response_scoring = requests.post(scoring_url, json=payload_scoring, headers=header)
print("Scoring response")
parsed = json.loads(response_scoring.text)
print(parsed)

for value in parsed['values']:
    confidence = value[11]
    prediction = value[13]
    print("Employee Attrition: {}\nConfidence: {}".format(prediction, confidence))
