import os
import json
import requests

CREDENTIALS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'adobe_config',
    'pdfservices-api-credentials.json'
)

def get_adobe_access_token(return_client_id=False):
    with open(CREDENTIALS_PATH) as f:
        creds = json.load(f)
    data = {
        "client_id": creds["client_credentials"]["client_id"],
        "client_secret": creds["client_credentials"]["client_secret"],
        "grant_type": "client_credentials",
        "scope": "openid,AdobeID,read_organizations,additional_info.projectedProductContext"    }
    resp = requests.post("https://ims-na1.adobelogin.com/ims/token", data=data)
    resp.raise_for_status()
    if return_client_id:
        return resp.json()["access_token"], creds["client_credentials"]["client_id"]
    return resp.json()["access_token"]