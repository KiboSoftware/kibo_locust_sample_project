# Sample Locust Project for Kibo web/api

## Setup
### install locust 
`  pip install -r requirements.txt `
### create the necessary datafiles/hostname directory

**assuming your Kibo Site is t123-s456.tpx.mozu.com**
```
    cp -R datafiles/sample-host-directory datafiles/t123-s456.tpx.mozu.com
```

```
project
│   README.md│  
│
└───confs
│   │   web.conf -- sample locust conf for running the web test
│   │   env.py -- sample locust conf for running the api test
│   
└───common
│   │   auth.py -- lib for authenticating 
│   │   env.py -- lib for parsing environent data
│      
└───datafiles   -- env/data files for your test hosts
│   │
│   └───hostname -- should map to the host name eg t123-s123.tpx....
│       │   env.json   -- api key and misc conf  * see below
│       │   content.csv  -- urls of contenet pages
│       │   products.csv   --- products
│       │   suggest_terms.csv  -- terms for suggest 
│       │   terms.csv  -- terms for serach
│       │   users.csv  -- logins
│
└───locustfiles
    │   api_get.py -- sample api get test
    │   file022.txt -- sample web test
```
### Host Data Directory
#### env.json 
**required fileds**
| field       | Description | Use | 
| ----------- | ----------- | ---- |
| auth_server | url to the kibo auth api       | API test
| app_id   | id or app key of the app in  [dev center](https://developer.mozu.com/console/app)        | API test
| app_secret   | app secret of the app in  [dev center](https://developer.mozu.com/console/app)        | API test
| ship_to   | array of ship to locations        | Web Test 
| payments   | array of payments         | Web Test

### Edit the conf files to match your host

## test run
### web
``` locust  --config confs/api_web.conf ```
### api
``` locust  --config confs/api_get.conf ```