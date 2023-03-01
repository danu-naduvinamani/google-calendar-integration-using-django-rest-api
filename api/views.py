from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os

# set environment variable for OAuth2
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# path to client secrets file downloaded from Google API console
CLIENT_SECRETS_FILE = "credentials.json"

# scopes to access Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

# callback URL to redirect to after authentication is complete
REDIRECT_URL = 'https://4073efd3-faa5-4bed-a66e-fd0739f947af.id.repl.co/rest/v1/calendar/redirect/'

# name and version of the Google Calendar API
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'


@api_view(['GET'])
def GoogleCalendarInitView(request):
  """
    View to initiate the Google Calendar OAuth2 flow
    """

  # create a new OAuth2 flow object from client secrets file and scopes
  flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

  # set the redirect URI for the OAuth2 flow
  flow.redirect_uri = REDIRECT_URL

  # generate an authorization URL to redirect the user to for consent
  authorization_url, state = flow.authorization_url(prompt='consent')

  # save the flow state in the user's session
  request.session['state'] = state

  # redirect user to the authorization URL
  return HttpResponseRedirect(authorization_url)


@api_view(['GET'])
def GoogleCalendarRedirectView(request):
  """
    View to complete the Google Calendar OAuth2 flow and retrieve events from the user's primary calendar
    """

  # get the flow state from the user's session
  state = request.session['state']

  # create a new OAuth2 flow object from client secrets file, scopes, and flow state
  flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE,
                                       scopes=SCOPES,
                                       state=state)

  # set the redirect URI for the OAuth2 flow
  flow.redirect_uri = REDIRECT_URL

  # get the authorization response from the request's full path
  authorization_response = request.get_full_path()

  # exchange the authorization code for a token and save the credentials in the user's session
  flow.fetch_token(authorization_response=authorization_response)
  credentials = flow.credentials
  request.session['credentials'] = request.session['credentials'] = {
    'token': credentials.token,
    'refresh_token': credentials.refresh_token,
    'token_uri': credentials.token_uri,
    'client_id': credentials.client_id,
    'client_secret': credentials.client_secret,
    'scopes': credentials.scopes
  }

  # check if credentials were successfully saved in the user's session
  if 'credentials' not in request.session:
    return redirect('rest/v1/calendar/init/')

  # create a new Google Calendar API service object using the saved credentials
  credentials = Credentials(**request.session['credentials'])
  service = build(API_SERVICE_NAME,
                  API_VERSION,
                  credentials=credentials,
                  static_discovery=False)

  # retrieve the user's upcoming events from their primary calendar
  events = service.events().list(calendarId='primary',
                                 maxResults=10,
                                 singleEvents=True,
                                 orderBy='startTime').execute()

  # if no events were found, return an error message
  if not events['items']:
    print('No data found.')
    return Response({"message": "No data found or user credentials invalid."})
  else:
    # if events were found, append each event to a list and return the list in the response
    events_list_append = []
    for events_list in events['items']:
      events_list_append.append(events_list)
      return Response({"events": events_list_append})
  # Return an error message if no events are found
  return Response({"error": "calendar event aren't here"})
