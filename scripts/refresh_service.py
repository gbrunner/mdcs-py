import logging
import logging.handlers
import time
import requests
import json

def refreshService(service):
    portal_url = "" #this is the server that is hosting the poral #services['portal']
    image_server_url = "" #This is the server that is hosting the image service #services['server']
    username = "un"#services['username']
    password = "pw"#services['password']

    # generate token
    token_payload = {'f': 'pjson', 'username': username, 'password': password, 'referer': portal_url}
    token_url = portal_url + '/sharing/rest/generateToken'

    token_request = requests.post(token_url, data=token_payload, verify=False)
    token = token_request.json()['token']

    # refresh service
    logging.info('Refreshing service {}'.format(service))

    sj_payload = {'f': 'pjson', 'token': token, 'serviceName': service, 'serviceType': 'ImageServer'}
    sj_url = image_server_url + '/rest/services/System/PublishingTools/GPServer/Refresh%20Service/submitJob'

    sj_request = requests.post(sj_url, data=sj_payload, verify=False)
    sj_jobId = sj_request.json()['jobId']

    # check job details
    check_job_payload = {'f': 'pjson', 'token': token}
    check_job_url = image_server_url + '/rest/services/System/PublishingTools/GPServer/Refresh%20Service/jobs/{}'.format(
        sj_jobId)
    status = ''

    while status != 'esriJobSucceeded':
        check_job_request = requests.post(check_job_url, data=check_job_payload, verify=False)
        status = check_job_request.json()['jobStatus']

        time.sleep(2)

    logging.info('Status = {} for {} '.format(status, service))
