# Ocean Simple seller

To setup the project run the following

```bash
git clone git@gitlab.com:datarella/MOBIX-GROUP/oceansimpleseller.git
cd oceansimpleseller || exit
make new_env
make install_env
```

To run the project you will need two terminals open simultaneously.

Export the following on vars on both of them:

```bash
export SELLER_AEA_KEY_ETHEREUM="0x4a7b2cc2d0a9574f9e207fcfb6b13f6daf4e90b9e0f50e389a68f507f9767880"
export SELLER_AEA_KEY_FETCHAI="1437aebfadbb766b810894a7859db3574088e6909f229e484e2e14e00b7c0875"

export BUYER_AEA_KEY_ETHEREUM="0xb6ad18f951812195b31f57f1ec2a79862885d3f5d3c84a1a0cc3c4d940a4cf9b"
export BUYER_AEA_KEY_FETCHAI="670c081eb3f674ae55e28ab714e7393abc74346a6fc738b1bf245140a038a3bb"

export STORJ_ENDPOINT="https://gateway.eu1.storjshare.io"
export STORJ_ACCESS_KEY="j2wulv3drlgrt5apjr2csc5lmkzyqpqakgzuoc63fn6wedxmnu2ng"
export STORJ_ACCESS_KEY_ID="jx7bgg74ceog3eznrovaiqcy23sa"
export TARGET_SKILL="eightballer/storj_file_transfer:0.1.0"
```

After the export on the first terminal run:
```bash
cd src || exit 
./run_ocean_seller.sh
```

On the second terminal run:
```bash
cd src || exit 
./run_ocean_buyer.sh
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
3. in project directory:
```bash
 pipenv shell # if you haven't already
 mkdocs serve
```
Visit http://127.0.0.1:8000/

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

