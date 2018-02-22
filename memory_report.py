import requests
import sys
from lxml import etree
import pprint

def get_server_status(base_url, user, password):
    '''
    base_url - string with the protocol, hostname and port without a trailing slash
    user - string username
    password - string password

    returns the string xml
    '''

    url = base_url + '/manager/status?XML=true'
    response = requests.get(url, auth=(user, password))
    if response.status_code != 200:
        raise Exception('Bad response from server when requesting status from ' + url + '. HTTP ' + str(response.status_code) + '. \n' + response.text)
    else:
        return response.content

def get_memory(status_bytes):
    '''
    status_bytes - bytes from a tomcat manager server status XML response
    returns a tuple of floats. The first float is the used memory. The second float is the max memory.
    ''' 
    status_doc = etree.XML(status_bytes)
    used_memory = float(status_doc.xpath("//status/jvm/memory/@total")[0])
    max_memory = float(status_doc.xpath("//status/jvm/memory/@max")[0])
    return (used_memory, max_memory)

def get_percent_memory_used(memory_tuple):
    '''
    memory_tuple - a tuple of floats whose first float is the used memory, and whose second float is the max memory.
    returns a float between 1 and 0 representing the percentage of memory used
    '''
    (used, max) = memory_tuple
    percent = used / max
    return percent 

def request_targets(base_url, user, password, relative_urls_file_path, requests_per_target):
    with open(relative_urls_file_path, 'r') as urls_file:
        target_url_paths = urls_file.readlines()

#overall_request_number, target_url, target_specific_request_number, response_status_code, post_request_memory_usage,
    for target_counter, target_url_path in enumerate(target_url_paths):
        target_url = base_url + target_url_path.strip()
        for target_specific_request_counter in range(0, requests_per_target):
            overall_request_number = (target_counter * requests_per_target) + target_specific_request_counter
            response = requests.get(target_url)
            response_status_code = response.status_code
            post_request_memory_usage = get_percent_memory_used(get_memory(get_server_status(base_url, user, password)))
            record = {
                'overall_request_number' : overall_request_number,
                'target_url' : target_url,
                'target_specific_request_number': target_specific_request_counter,
                'response_status_code' : response_status_code,
                'post_request_memory_usage' : post_request_memory_usage
            }
            pprint.pprint(record, width=1)


if __name__ == "__main__":
    if len(sys.argv) < 5 or len(sys.argv) > 6:
        print("Usage: python memory_report.py $BASE_URL_FOR_TOMCAT_INSTANCE $TOMCAT_MANAGER_USER $TOMCAT_MANAGER_PASSWORD $PATH_TO_FILE_WITH_RELATIVE_URLS $OPTIONAL_TIMES_TO_REPEAT_EACH_REQUEST")
        print("Example Usage:")
        print("python memory_report.py http://my-server.com:80 tcAdmin p@ssw0rd my_urls.txt 42")
        exit(1)
    else:
        base_url = sys.argv[1]
        user = sys.argv[2]
        password = sys.argv[3]
        relative_urls_file_path = sys.argv[4]
        if len(sys.argv) == 6:
            request_repetition = int(sys.argv[5])
        else:
            request_repetition = 1

        request_targets(base_url, user, password, relative_urls_file_path, request_repetition)
