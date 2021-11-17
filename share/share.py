#!/usr/bin/python

import argparse
import http.client as httplib
import httplib2
import os
import random
import time

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow


# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# TODO: move this to a more generic file along with resumeable_upload
# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
    httplib.IncompleteRead, httplib.ImproperConnectionState,
    httplib.CannotSendRequest, httplib.CannotSendHeader,
    httplib.ResponseNotReady, httplib.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
# TODO: find out the right way to load secrets / keys (env variable?)
CLIENT_SECRETS_FILE = "client_secret.json"

# OAuth 2.0 Access scope limits app access to authenticated user's channel
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Video file to upload")
    parser.add_argument("--title", help="Video title", default="Test Title")
    parser.add_argument("--description", help="Video description", default="Test Description")
    parser.add_argument("--category", default="22", help="Numeric video category. " +
        "See https://developers.google.com/youtube/v3/docs/videoCategories/list")
    parser.add_argument("--keywords", help="Video keywords, comma separated", default="")
    parser.add_argument("--privacyStatus", choices=VALID_PRIVACY_STATUSES,
        default="private", help="Video privacy status.")
    return parser.parse_args()


# Authorize the request and store authorization credentials.
def get_authenticated_service():
    # TODO: remove this unnecessary bullshit
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    # type google.oauth2.credentials.Credentials
    credentials = flow.run_console()

    # builds googleapi object, in this case an instance of a youtube object that 
    # has youtube api methods
    service_build = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    return service_build 

def initialize_upload(youtube, options):
    tags = None
    if options.keywords:
        tags = options.keywords.split(",")

    body={
            "snippet": {
                "title": options.title,
                "description": options.description,
                "tags": tags,
                "categoryId": options.category
            },
            "status": {
                "privacyStatus": options.privacyStatus
            }
        }

# Call the API"s videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(part=",".join(body.keys()), body=body,
        media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True))
    # insert_request is of type googleapiclient.http.HttpRequest

# The chunksize parameter specifies the size of each chunk of data, in
# bytes, that will be uploaded at a time. Set a higher value for
# reliable connections as fewer chunks lead to faster uploads. Set a lower
# value for better recovery on less reliable connections.

    resumable_upload(insert_request)

# TODO: this seems generic enough to move elsewhere
# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print(f"Uploading file...")
            status, response = request.next_chunk()
            if response is not None:
                if "id" in response:
                    print(f"Video id {response['id']} uploaded successfully.")
                else:
                    exit(f"The upload failed with an unexpected response: {response}")
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f"A retriable HTTP error {e.resp.status} occurred:\n{e.content}" 
            else:
                raise

        except RETRIABLE_EXCEPTIONS as e:
            error = f"A retriable error occurred: {e}"

        if error is not None:
            print(f"{error}")
            retry += 1
            if retry > MAX_RETRIES:
                exit(f"No longer attempting to retry.")

            # TODO: Seems arbitrary
            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print(f"Sleeping {sleep_seconds} seconds and then retrying...") 
            time.sleep(sleep_seconds)

def main():
    args = parse_args()
    youtube = get_authenticated_service()

    try:
        initialize_upload(youtube, args)
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")

main()
