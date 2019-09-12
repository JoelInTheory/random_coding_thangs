# About
This is a simple coding practice exercise making a user / group list
The data is stored in a local sqlite db saved in `yousirs/backends/data/you_sirs.db` by default
If you set an environment variable of `DATABASE_URL` to a valid sqlalchemy connection string,
it will try to use that instead.

## Installation
requires:
- python 3
- flask
- flask-restful
- gunicorn
- some of the other usual suspecs (see requirements.txt)

There is a simple bash helper script if you are running this locally that will try to create
a virtualenv for you, activate it, and install the pip requirements. 

To use that, run:
- `source make_yousirs_venv.sh`

with the requirements installed you can launch a local web server serving the application via:
```
gunicorn yousirs:app
```
a more helpful launch command might be:
```
gunicorn --access-logfile - --log-level debug --bind 0.0.0.0:8000 yousirs:app
```


it should be available on `localhost:8000` by default

Alternatively this app is packaged for deployment to Heroku. If you were to ask around, there may
already be a deployment ready for you to use. The heroku branch of this repo is setup to trigger an automatic deploy.

*Note: currently the Heroku deployments for this app are setup with a postgres DB attached so the data persists.*
*If you setup the app on your own and do not configure a DATABASE_URL environment VAR with a connection string,*
*the app will default to sqlite and the data will be lost on any dyno restart ore deploy*

## SPEC
once running the following calls can be made:

**/users**
 - **GET** list of users
 - **POST** create user (not assigned to any groups)
```
body: {'first_name': <string>, 'last_name': <string>, 'userid': <userid>}
```

**/users/\<userid\>**
- **GET** get information for <userid\>
- **DELETE** delete \<userid>
- **PUT** update user information
 - all values required
 ```
 body: {'first_name': <new first_name>, 'last_name': <new last_name>, 'userid': <new userid>}
 ```
 
**/groups**
 - **GET** list of groups
 - **POST** create empty group
   -  `body: {'groupname': <string>}`

**/groups/<groupid\>**
- **GET** get information for <groupid\>
- **DELETE** delete \<groupid>
- **PUT** add list of users as members of <groupid\>
  - accepts json list as body
  - curl example: 
    ```bash
    curl -X PUT \
    -H 'Content-Type: application/json' \
    localhost:8000/groups/muppets \
    -d '["animal", "kermit"]'
    ```

## Bundled Tests
edit `yousirs/config.py` with appropriate host / port (default localhost / 8000) and run

**python yousirs/run_tests.py**

you may also pass a couple optional arguments to facilitate testing:
- `--slow` (pauses for input between each test) 
- `--verbose` (does a full get on users / groups after each test and displays results)

**python yousirs/run_tests.py --slow --verbose**

Example output (without verbose / slow for brevity)

```
$ python yousirs/run_tests.py 
----------------------------------------------------------------------------------------------------
user_list_empty                    : OK - empty user list
----------------------------------------------------------------------------------------------------
group_list_empty                   : OK - empty group list
----------------------------------------------------------------------------------------------------
user_post_malformed                : OK - expected 400 received
----------------------------------------------------------------------------------------------------
user_post                          : OK - user create successful
<snip>
```
