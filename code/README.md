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

### Heroku Setup

1. Go to [Heroku](https://www.heroku.com/) and Sign-Up/login for free.
2. [Heroku Dashboard](https://dashboard.heroku.com/apps) -> `New` -> `Create new app`
3. Key in the `App name` (e.g., `ntuoss-api-test`) ->  `Create app`
4. Go to [Account Settings](https://dashboard.heroku.com/account) -> `API Key` -> `Reveal`. Copy the API key. 

### GitHub Actions Setup
1. Fork [this](https://github.com/guptajay/NTUOSS-API-Development-Workshop) repository.
2. Go to your Repository `Settings` -> `Secrets (Actions)` (under `Security` tab) -> `New repository secret`
3. Key in `Name`: `HEROKU_API_KEY` and `Value`: `<YOUR_HEROKU_API_KEY>` -> `Add secret` 
4. Go to `.github/workflows/main.yml` and change the following.
    - `heroku_app_name: "<your_heroku_app_name>"`
    - `heroku_email: "<your_heroku_account_email>"`
    - `healthcheck: "https://<your_heroku_app_name>.herokuapp.com/healthcheck"`
5. Push the changes to GitHub to trigger the deployment workflow. 

### Run Live Server
> Run the Uvicorn live server to serve the API

```console
$ uvicorn main:app --reload
```
