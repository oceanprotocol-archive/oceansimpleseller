# AEA Storj File Uploader

to setup the project

```
git clone git@gitlab.com:datarella/MOBIX-GROUP/storj-aea.git
make new_env
make install_env
```

to run the project

```
make run_app
```


# Components

- gitlab ci
    - The ci contains the basic configuration required to launch a launch a gitlab ci
  
- Dockerfile
  - Basic Dockerfile which installs deps and launchs the app

- makefile
  - lints
      - isort
      - black
      - code clean
- pre-commit hooks for the build process

- scripts
  - app.py launcher for debugging and launching docker process

- Pipfile

- gitignore
- docker ignore
- .env file
- docs


# Example running docs

1. clone repo
2. setup a new environment
   - make new_env
   - make 
3. run application
```bash
 RUN_CMD="echo hello" pipenv run app
```


# Install environment
1. install pip
```
pip install pipenv
```

2. create new environment
```
make new_env
```
3. install new env
```
make install_env
```




# dev tools
setup pre-commit hooks
```
make install_hooks
```

lint, format, and sense check code
```
make lint
```

run tests

```
make tests
```

