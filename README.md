# Python Application for a Webex Teams Integration

## Python Sampler

### Splash Page
A simple plash page with a 'Sign In' button that triggers the Oauth process if no token is stored in the session.
![Splash Page](https://user-images.githubusercontent.com/11665315/40385446-95227e1c-5dd4-11e8-8192-0e126b684a6c.png)

### Login
Login via Webex Teams
![Login Page](https://user-images.githubusercontent.com/11665315/40385449-97acfc3e-5dd4-11e8-87c1-212401925b88.png)

### Display Target Page
Render a target page (in this case /hello) in which you have the token data in the session. This page utilizes the [Python Webex Teams API](https://github.com/CiscoDevNet/ciscosparkapi/tree/master/ciscosparkapi) to get the user's display name and render that to the page.
![Target/Hello Page](https://user-images.githubusercontent.com/11665315/40385455-9aa097ca-5dd4-11e8-8592-52e0ca738000.png)

## Use the Demo
[Heroku Hosted Demo](https://webexteamspyoauth.herokuapp.com/) that utilized the **gmail** org. Email addresses that do not end in **@gmail.com** will not result in a successful login.

## Quick Deploy 
1. Create a [Webex Teams Integration](https://developer.webex.com/add-integration.html): the redirect url will be <code>https://<your_heroku_app_name>.herokuapp.com/callback</code>. Don't navigate away, you'll need some details to deploy to heroku.
2. [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
