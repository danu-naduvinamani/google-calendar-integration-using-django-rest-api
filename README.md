# Google Calendar Integration Using Django REST API Framework
This Django project integrates with the Google Calendar API using the google-auth, google-auth-oauthlib, and google-auth-httplib2 libraries to handle authentication and authorization, and the google-api-python-client library to interact with the API.
## Getting Started

To get started with this project, follow these steps:

1.Clone the repository to your local machine:

```https://github.com/danu-naduvinamani/google-calendar-integration-using-django-rest-api.git ```

2.Install the required Python packages:

```pip install -r requirements.txt```

3.Set up a Google Cloud Console project and download the JSON credentials file. Follow the Google Calendar API Python Quickstart guide to learn how to set up your project and download the credentials.

4.Rename the credentials file to `credentials.json` and place it in the project root directory.

5.Run the Django development server:

```python manage.py runserver```

The API will be available at 'http://127.0.0.1:8000/rest/v1/calendar/init/'.

## API Endpoints

This project implements two API endpoints for interacting with the Google Calendar API:

```/rest/v1/calendar/init/```

This endpoint initiates the OAuth2 authorization flow and redirects the user to the Google OAuth2 consent screen.

Request Method: GET

Response:

302 Found - If the user is not authenticated, the server will redirect to the Google OAuth2 consent screen.

```/rest/v1/calendar/redirect/```

This endpoint handles the OAuth2 callback and exchanges the authorization code for an access token.

Request Method: GET
Response:

200 OK - Returns a JSON response containing the authenticated user's events from their primary calendar.
## Screenshots
#### OAuth2 Consent Screen
![authscreen](https://user-images.githubusercontent.com/126635832/222046869-ec84645c-0f47-471a-80cb-f98d78d1628e.jpg)
#### Calendar Events API Endpoint
![Screenshot (21)](https://user-images.githubusercontent.com/126635832/222046944-b9e3297e-38af-43d4-8118-7370cb7d6be2.png)
