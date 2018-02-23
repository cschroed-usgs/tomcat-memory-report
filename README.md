# Tomcat Memory Report

## Purpose
This script hits URLs on a tomcat server and prints the % memory usage for that tomcat instance after each request. The URLs are loaded from a parameterized file. The file should contain one relative URL per line. The URLs are expected to be relative to the base URL.

## Usage:

 * Create a python virtualenv.
 * Install the dependencies required in the `requirements.txt`.
 * Track down the protocol, hostname, and port of your tomcat server.
 * If necessary, add a user to your tomcat with the manager-status role. Get the credentials for this user.
 * Create a file with a bunch of URLs -- one per line. The URLs should be relative to the port of your tomcat server.
 * By default the script makes one request per URL. You can hit the same URL multiple times by tacking on an additional integer parameter.
 * Now run the script using the information you gathered above.

```
python memory_report.py $BASE_URL_FOR_TOMCAT_INSTANCE $TOMCAT_MANAGER_USER $TOMCAT_MANAGER_PASSWORD $PATH_TO_FILE_WITH_RELATIVE_URLS $OPTIONAL_TIMES_TO_REPEAT_EACH_REQUEST
```


### Example:

```
git clone ...
cd <repo>
virtualenv env
. env/bin/activate
pip install -r requirements.txt
python memory_report.py http://my-server.com:80 tcAdmin p@ssw0rd my_urls.txt 2
```

Where `my_urls.txt` is a file with contents:

```
/contextPath/version
/contextPath/favico.ico
/contextPath/index.jsp
```

The output looks like:

```
{'overall_request_number': 0,
 'post_request_memory_usage': 0.5736009564748819,
 'response_status_code': 200,
 'target_specific_request_number': 0,
 'target_url': 'http://my-server.com:80/contextPath/version'}
{'overall_request_number': 1,
 'post_request_memory_usage': 0.5736009564748819,
 'response_status_code': 200,
 'target_specific_request_number': 1,
 'target_url': 'http://my-server.com:80/contextPath/version'}
{'overall_request_number': 2,
 'post_request_memory_usage': 0.5736009564748819,
 'response_status_code': 200,
 'target_specific_request_number': 0,
 'target_url': 'http://my-server.com:80/contextPath/favico.ico'}
...
```


### Simulating Production Requests
If your tomcat is configured to log basic HTTP request information, you can extract the URLs from your logs.

```
$> cut -f 7 access_log.2018-02-20.log | grep '^GET' | sed 's/^GET //' | sed 's/ HTTP\/1.1$//' | head -n 5
/myContextPath/ABC/sos?request=GetObservation&featureId=311909305001
/myContextPath/DEF/wfs?request=GetFeature&featureId=10
/myContextPath/GHI/qw?mimeType=xml&siteid=61060851495047
/myContextPath/JKL/sos?request=GetObservation&featureId=374139
/myContextPath/MNO/qw?mimeType=xml&siteid=40619700
```

## Limitations
 * This script only supports HTTP GET requests.
