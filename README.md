# garnbarn-backend

[![Build Status](https://app.travis-ci.com/GarnBarn/garnbarn-backend.svg?branch=master)](https://app.travis-ci.com/GarnBarn/garnbarn-backend)
[![codecov](https://codecov.io/gh/GarnBarn/garnbarn-backend/branch/master/graph/badge.svg?token=HG7J0R5C2J)](https://codecov.io/gh/GarnBarn/garnbarn-backend)

## 📦 Build Steps

### 1. Config the env file

You can follow these step in [document](https://garnbarn.github.io/garnbarn-backend/#/?id=setting-up-env)

### 2. Config Credential Files

#### 2.1 Add Firebase Admin SDK Service Account

There are 2 ways to do this:

1. In project root directory. Create file named `firebase-adminsdk-credential.json` that contain the credential from Firebase.
2. Set the `GOOGLE_APPLICATION_CREDENTIAL` env variable to equal to the path to the credential file.

> The application will load the `firebase-adminsdk-credential.json` first. If this file is not found, It will continue to use the file from env variable named `GOOGLE_APPLICATION_CREDENTIAL`

If no credential, The API will always return 500 Internal Server Error as its response.

#### 2.2 Add LINE Platform secret config

This file contain credential from LINE Login and LINE Messaging API Platform. You can generate these credential from [LINE Developer Console](https://developers.line.biz/en/)

1. Create file name `line-config.json` with this structure

```json
{
  "login": {
    "channel_secret": "00000",
    "channel_id": "00000"
  },
  "messaging_api": {
    "channel_access_token": "00000"
  }
}
```

### 3. Serve (locally)

In the top level folder of the project.

```bash
$ python manage.py runserver
```

### 4. Serve in production

Since Django don't serve the static file while in production mode (`DEBUG=False`). So you need to have the CDN to provide the CSS and JS file from Admin page

To collect the static file for admin page

1. Call this command

```bash
$ python manage.py collectstatic
```

2. The Django will create folder named `static/` at the top level folder of the project. Copy that file to serve it in your CDN.

3. Update the config named `STATUC_URL` to equal to the URL to your CDN.
