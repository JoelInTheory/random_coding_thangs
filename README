# About
This is a simple coding practice exercise making a user / group list
The data is stored in a local sqlite db saved in `yousirs/backends/data/you_sirs.db`

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
source make_yousirs_venv.sh

with the requirements installed you can launch a local web server serving the application via:
gunicorn yousirs:app

it should be available on `localhost:8000` by default

Alternatively this app is packaged for deployment to Heroku. If you were to ask around, there may
already be a deployment ready for you to use. 
*Note: since this is using a local sqlite db to keep it simple, the data will be lost if the Heroku dynos were to ever restart, or a deploy occurs.*

## SPEC
once running the following calls can be made:
**/users**
   - **GET** - list of users
	   - ```curl -X GET <endpoint>/users -H 'Content-Type: application/json```
    - **POST** - create user (not assigned to any groups)
		    - ```body: {'first_name': <string>, 'last_name: <string>, 'userid': <userid>```

**/users/\<userid\>**
- **GET** - get information for <userid\>
- **DELETE** - delete \<userid>
- **PUT** - update user information
		- ```body: {'first_name': <new first_name>, 'last_name: <new last_name>, 'userid': <new userid>```
		- all values required

**/groups**
	- **GET** - list of groups
	- **POST** - create empty group
	-  ```body: {'groupname': <string>}```

**/groups/<groupid\>**
- **GET** - get information for <groupid\>
- **DELETE** - delete \<groupid>
- **PUT** - add list of users as members of <groupid\>
		- accepts json list as body
		- curl example: 
		 `curl -X PUT \`
		 `-H 'Content-Type: application/json' \`
		` localhost:8000/groups/muppets \`
		 `-d '["animal", "kermit"]'`

## Bundled Tests
edit `yousirs/config.py` with appropriate host / port (default localhost / 8000) and run
**python yousirs/run_tests.py**
you may also pass the `--slow` (pauses for input between test) 
and `--verbose` (does a full get on users / groups after each test)
**python yousirs/run_tests.py --slow --verbose**
Example output (without verbose / slow for brevity)
```$ python yousirs/run_tests.py 
----------------------------------------------------------------------------------------------------
user_list_empty                    : OK - empty user list
----------------------------------------------------------------------------------------------------
group_list_empty                   : OK - empty group list
----------------------------------------------------------------------------------------------------
user_post_malformed                : OK - expected 400 received
----------------------------------------------------------------------------------------------------
user_post                          : OK - user create successful
<snip>```
