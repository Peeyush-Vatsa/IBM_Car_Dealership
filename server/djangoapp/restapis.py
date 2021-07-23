import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        print("A network error has occured")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST from {} ".format(url))
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("A network error has occured")
    status_code = response.status_code
    print("With status code {} ".format(status_code))

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        results = json_result["dealerships"]
        if 'id' in kwargs.keys():
            refined_results = []
            for dictionary in results:
                if kwargs['id'] == dictionary.id:
                    refined_results.append(dictionary)
                    break
            return refined_results
        elif 'state' in kwargs.keys():
            refined_results = []
            for dictionary in results:
                if kwargs['state'] == dictionary.st:
                    refined_results.append(dictionary)
            return refined_results
    return results

def get_review_from_cf(url, **kwargs):
    results = []
    json_results = get_request(url)
    if json_results:
        results = json_results['reviews']
        if 'dealerId' in kwargs.keys():
            refined_results = []
            for dictionary in results:
                if dictionary['dealership'] == kwargs['dealerId']:
                    refined_results.append(dictionary)
            return refined_results
    return results

def get_sentiment(review):
    auth = IAMAuthenticator('UhXf6k8wOefKH0pkrY-hQr-3AUEOwmCDYlYazxdJ8MBJ')
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-03-05', authenticator=auth)
    natural_language_understanding.set_service_url("https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com")
    sentiment_raw_json = natural_language_understanding.analyze(text=review, features=Features(sentiment=SentimentOptions(document=True))).get_result()
    print(sentiment_raw_json)
    sentiment_raw = json.dumps(sentiment_raw_json)
    sentiment = sentiment_raw_json['sentiment']['document']['label']
    return sentiment



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



