## Introduction to API Development

### Virtual Environment Setup

#### MacOS & Linux

```console
$ python3 -m venv env 
$ source env/bin/activate
$ pip install -r requirements.txt
```

#### Windows

```console
> pip install virtualenv 
> virtualenv env
> pip install -r requirements.txt
```

### Railway Setup

1. Go to [Railway](https://railway.app/) and Sign-Up/login for free.
2. [Railway Dashboard](https://railway.app/dashboard) -> `New Project` -> `Deploy from GitHub Repo`
3. Follow the on-screen instructions to connect your GitHub account to Railway. 
3. Select the GitHub `Repository Name` (e.g., `SMU.hack-API-Development`) ->  `Deploy now`
4. Go to `Project Settings`(https://dashboard.heroku.com/account) -> `Generate Domain`
5. Go to the `deployment url` to preview the API. 

### GitHub Actions Setup
1. Fork [this](https://github.com/guptajay/SMU.hack-API-Development) repository.
2. Push the changes to GitHub to trigger the deployment workflow. 

### Run Live Server
> Run the Uvicorn live server to serve the API

```console
$ uvicorn main:app --reload
```
