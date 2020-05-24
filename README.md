# find-similar-artists

A flask app that takes an artist as an input and generates a Spotify playlist of top songs of artists recommended based on the input.
Can use the Spotify API or https://music-map.com for sourcing the recommended artists.

git Live demo at https://find-similar-artists.herokuapp.com/

## How to setup development environment
### Requirements
Python 3 & virtualenv (recommended)
### Steps
Clone the repository and cd into the directory:
```
git clone https://github.com/hur/find-similar-artists.git
cd find-similar-artists
```
Set up a virtual environment:

`virtualenv venv`

Activate the virtual environment:
```
(Windows / CMD):
venv\Scripts\activate
(Mac OS / Unix):
source venv/bin/activate 
```
Install requirements:

`pip install -r requirements.txt`

Set up `.env` file with the needed keys:

```
SECRET_KEY = "yoursecretkey"
SPOTIFY_CLIENT_ID="clientid"
SPOTIFY_CLIENT_SECRET="clientsecret"
SPOTIFY_CALLBACK_URL="callbackurl"
REDIS_URL="redisurl"
```
You can generate a random secret key using Python:
```
>>> import uuid
>>> uuid.uuid4().hex
```

You need to create an app and get its client id and secret at https://developer.spotify.com/.
Furthermore, you need to add callback url for `localhost:5000/callback` and add it in the spotify dashboard as well as the .env
file. 


Run the app using `flask run`. In some cases using `python -m flask run` instead may resolve issues that occur with `flask run`.
In another terminal tab, run an rq worker using `rq worker`. This will process the jobs sent to the task queue.

For running all tests, use `py.test`

