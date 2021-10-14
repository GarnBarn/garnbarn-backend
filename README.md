# GarnBarn

> Homework/Task manager so you can manage your time better.

This document contains instruction on how to setup and use the API.  
You can jump to the content using the navigation bar on your left.

# Setting up .env

By creating .env you can create your own external config which include
  - SECRET_KEY
  - DEBUG
  - ALLOW_HOST
  - TIME_ZONE

## Secret key configuration

In .env you can add a secret key by adding
```
  SECRET_KEY = your_secret_key
```

> By default SECRET_KEY = no_secret_key

## Allow debuging

Allow debuging by adding
```
  DEBUG = True
```

> By default DEBUG = False

## Adding host

To adjust host that can access the site
```
  ALLOW_HOST = [host_1, host2, ...]
```

> By default ALLOW_HOST = [localhost, 127.0.0.1]

## Set time zone

```
TIME_ZONE = my_time_zone
```

> By default TIME_ZONE



