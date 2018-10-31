# youtubeapi

It allows user to enter a search term in the UI and the resultant items are searched and displayed using YouTube Data API v3.
The results are sortable based on 2 params name and published date.

### Requirements
* Python 2.6 or greater.
* The pip package management tool.
* Access to the internet and a web browser.
* A Google account.

## Before Using YouTube Data API v3 :

    1.You need a Google Account to access the Google API Console, request an API key, and register your application.
    Click - https://console.developers.google.com/flows/enableapi?apiid=youtube

    2.Create a project in the Google Developers Console or Select Already made Project Click Continue, then Go to credentials,Click on Credentials on side bar.

    3.At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button.

    4.Select the Credentials tab, click the Create credentials button and select OAuth client ID.

    5.Select the application type Web application and enter the name "YouTubeApi". 
    
    6.Follow the instructions to enter JavaScript origins, redirect URIs, or both.
    ForEx-  A.  Set Authorized JavaScript origins as 
                 	http://localhost:5000
                    https://localhost:5000 
            B.  Set  Authorized redirect URIs
                    http://localhost:5000/oauth2callback 
                    https://localhost:5000/oauth2callback 

    7.Click the Create button.

    8.Click the file_download (Download JSON) button to the right of the client ID.

    9.Move the downloaded file to your working directory and rename it client_secret.json.




## Run the program :

1.Make Virtual environment.

```
$ python3 -m venv flask
$ source flask/bin/activate
```

2.Run 

```
$ pip install -r requirements.txt
$ python3 run.py
```








