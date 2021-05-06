import requests
import os
from dotenv import load_dotenv
from os.path import join, dirname
load_dotenv(join(dirname(__file__), '../.env'))


''' REQUIREMENTS: have server running on localhost:5000 '''

def test_authenticated_request():

    res = requests.get(
        url=f"http://localhost:5000/?key={os.environ['API_KEY']}", 
    )
    assert res.status_code == 200

    print("Authenticated request test passed")


def test_unauthenticated_request():

    res = requests.get(
        url="http://localhost:5000" 
    )
    assert res.status_code == 401

    print("Unauthenticated request test passed")


def test_get_adjacent_nodes():
    res = requests.get(
        url=f"http://localhost:5000/api/adjacent_nodes?key={os.environ['API_KEY']}", 
    )
    print(res.text)
    assert res.status_code == 200
    print("Get adjacent nodes test passed")


def test_authenticated_req_enumerations_get():

    res = requests.get(
        url=f"http://localhost:5000/api/enumerations?key={os.environ['API_KEY']}", 
    )
    print(res.text)
    assert res.status_code == 200


    print("Authenticated request test passed")