from selenium import webdriver
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import os
import json
from selenium.webdriver.common.by import By
import time

 

projectId="2676a93a-4711-4bc0-9880-9b4f5fb90d07"
BROWSERBASE_API_KEY="bb_live_P5hwEr2ge_5VFr8PJhEzmlkHk8E"
# def create_session():
#     url = "https://www.browserbase.com/v1/sessions"
#     headers = {
#         "Content-Type": "application/json",
#         "x-bb-api-key": "bb_live_P5hwEr2ge_5VFr8PJhEzmlkHk8E",
#     }
#     json = {
#         "projectId": "2676a93a-4711-4bc0-9880-9b4f5fb90d07",
#         "browserSettings": {
#           # Fingerprint options
#           "fingerprint": {
#             "devices": ["mobile"],
#                 "locales": ["en-US"],
#                 "operatingSystems": ["android"],
#             },
#         },
#     }
#     response = requests.post(url, json=json, headers=headers)
#     return response.json()["id"]

def create_session():
    url = 'https://www.browserbase.com/v1/sessions'
    headers = {'Content-Type': 'application/json', 'x-bb-api-key': BROWSERBASE_API_KEY}
    response = requests.post(url, json={ "projectId": projectId }, headers=headers)
    return response.json()['id']

class CustomRemoteConnection(RemoteConnection):
    _session_id = None

    def __init__(self, remote_server_addr: str, session_id: str):
        super().__init__(remote_server_addr)
        self._session_id = session_id

    def get_remote_connection_headers(self, parsed_url, keep_alive=False):
        headers = super().get_remote_connection_headers(parsed_url, keep_alive)
        headers.update({"x-bb-api-key": "bb_live_P5hwEr2ge_5VFr8PJhEzmlkHk8E"})
        headers.update({"session-id": self._session_id})
        # enable proxy here
        headers.update({"enable-proxy": "true"})
        return headers

def run():
    session_id = create_session()
    custom_conn = CustomRemoteConnection(
        "http://connect.browserbase.com/webdriver", session_id
    )
    options = webdriver.ChromeOptions()
    options.debugger_address = "localhost:9223"
    driver = webdriver.Remote(custom_conn, options=options)
    cookies = parse_cookies(open('cok.txt','r').read())
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
            
        except:
            pass
        else:
            print("cookie added")
    run_script(driver)

    driver.save_screenshot('test.png')

    # Make sure to quit the driver so your session is ended!
    driver.quit()

run()
