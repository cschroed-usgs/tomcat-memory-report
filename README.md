# Tomcat Memory Report

## Purpose
This script hits URLs on a tomcat server and prints the % memory usage for that tomcat instance after each request. The URLs are loaded from a parameterized file. The file should contain one relative URL per line. The URLs are expected to be relative to the base URL.

## Usage:

 * Create a python virtualenv.
 * Install the dependencies required in the `requirements.txt`.
 * Track down the protocol, hostname, and port of your tomcat server.
 * If necessary, add user to your tomcat with the manager-status role. Get the credentials for this user.
 * Create a file with a bunch of URLs -- one per line. The URLs should be relative to the port of your tomcat server.
 * Now run the script using the information you gathered above.

```
python memory_report.py $BASE_URL_FOR_TOMCAT_INSTANCE $TOMCAT_MANAGER_USER $TOMCAT_MANAGER_PASSWORD $PATH_TO_FILE_WITH_RELATIVE_URLS")
```

### Example:

```
git clone ...
cd <repo>
virtualenv env
. env/bin/activate
pip install -r requirements.txt
python memory_report.py http://my-server.com:80 tcAdmin p@ssw0rd my_urls.txt
```

Where `my_urls.txt` is a file with contents:

```
/contextPath/version
/contextPath/favico.ico
/contextPath/index.jsp
```

