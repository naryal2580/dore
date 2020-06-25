
__version__ = 0.001

from requests import request as _request
import urllib3 as _urllib3
from hashlib import sha512
from .extra import *
from requests.structures import CaseInsensitiveDict as case_insensative_dict
import re as regex
import json
from threading import Thread as _Thread
from .style import *


RETRIES = JUICE = {}


def request(url='', method='get', params={}, data={}, json={}, headers={}, cookies=None, files=None, auth=None, timeout=None, verify=True, proxies='socks5://127.0.0.1:9050', follow_redirects=True, local=False, max_retries=5):
    """
    Request with proxies, `socks5://localhost:9050` by default and return the response (requests.model.Response)
    
    NOTE: Defaults to `get` http method, and if data/json/files are passed then defaults to `post`
    NOTE: Auto adds scheme `http` (insecure) if no scheme passed

        Parameters:
            url (str): URL to request (eg.: 'https://httpbin.org')
            method (str): HTTP Method to use (eg.: 'post')
            params (dict): URL parameters to use (eg.: {'q': 'test'} == `https://httpbin.org/get/?q=test`)
            data (dict): Request body data to use (eg.: {'id': 99})
            json (dict): Request JSON body to use (eg.: {'user': 'name', 'pass': 'word})

            ... (Reffer to `requests` docs.)

            verify (bool): Verify SSL/TLS certificates
            proxies (str/dict): Dictionary of proxies to use, or String of a proxy to be used for both http, https
            follow_redirects (bool): Shall redirecties be followed
            local (bool): If its True, it'll bypass proxies in use
            max_retries (int): Maximum number of retries to be made on errors

        Returns:
            response (requests.model.Response): HTTP Response of the specific class "mentioned" FROM the request made.
    """
    global RETRIES
    # print(url, method, params, data, json, headers, cookies, files, auth, timeout, proxies, local, max_retries)
    if not url:
        return None
    if proxies and type(proxies) == dict:
        PROXIES = proxies
    if type(proxies) == str:
        PROXIES = {
            'http': proxies,
            'https': proxies
        }
    scheme = url.split('://')[0]
    if len(url.split('://')) == 1:
        scheme = 'http'
        url = f'{scheme}://{url}'
    if scheme not in ('http', 'https'):
        raise TypeError(bad(f'{scheme} -> does not look like HTTP(S) url'))
    if data or json or files:
        method = 'post'
    if headers:
        if not 'User-Agent' in headers:
            headers['User-Agent'] = f'dore/{__version__}'
    else:
        headers = {'User-Agent': f'dore/{__version__}'}
    if not verify:
        # print(warn('Insecure requests (NO TLS/SSL CERT VERIFICATION) -> Enabled'))
        _urllib3.disable_warnings(_urllib3.exceptions.InsecureRequestWarning)
    if local:
        # print(warn('Local mode enabled (NO PROXIES BEING USED) -> `renew()` will not work'))
        PROXIES = {}
    if scheme == 'http':
        pass
        # print(warn('Not a TLS request -> Using an insecure protocol'))
    request_hash = sha512(bytify(locals())).hexdigest()
    if request_hash not in RETRIES:
        RETRIES[request_hash] = 0
    try:
        RETRIES[request_hash] += 1
        if max_retries >= RETRIES[request_hash]:
            response =  _request(
                                method,
                                url,
                                params=params,
                                data=data,
                                json=json,
                                headers=headers,
                                cookies=cookies,
                                files=files,
                                auth=auth,
                                timeout=timeout,
                                proxies=PROXIES,
                                verify=verify,
                                allow_redirects=follow_redirects
                            )
            del RETRIES[request_hash]
            return response
    except Exception as err:
        if proxy_works(PROXIES):
            print(bad(f'Error [{RETRIES[request_hash]}] -> {err}'))
            response =  request(
                                url,
                                method,
                                params,
                                data,
                                json,
                                headers,
                                cookies,
                                files,
                                auth,
                                timeout,
                                verify,
                                proxies,
                                follow_redirects,
                                local,
                                max_retries
                            )
            try:
                del RETRIES[request_hash]
            except KeyError: # I don't know what's wrong here :(
                pass
            return response
        else:
            if PROXIES:
                print(bad('Bruh! -> Check if the proxy is working properly..'))


def match(method='regex', object1=None, object2=None):
    """
    Tries to check if content of object1 == object2
    methods = ('regex', 'length', 'headers', 'json', 'resp_code')

        Returns:
            bool: Boolean if, content of those objects match

        Parametes:
            method (str): Method for the match to work with
        
                if method is 'regex:
                    NOTE: Content of both objects are automatically converted into bytes-like object
                    object1: Response content / Response object for comparision
                    object2: Regex pattern for the comparision
        
                if method is 'length':
                    NOTE: Content of both objects are automatically converted into bytes-like object
                    object1: Object whoose length needs to be compared with
                    object2: Length, or any object with length
                
                if method is 'headers':
                    NOTE: Content of object1 is automatically converted into case insensative `dict` object
                    object1: Object whoose HTTP headers needs to be compared
                    object2 (dict/list): Dictionary of headers to match from the response (uses regex on values)

                        if type(object2) is list or tuple:
                            # **ONLY** checks if the list of passed headers are present (keys check)
                
                if method is 'json':
                    NOTE: Content of object1 is automatically converted into case insensative `dict` object
                    object1: Object whoose JSON response needs to be compared with
                    object2: JSON to compare response json with (uses regex on values)

                        if type(object2) is list or tuple:
                            # Will only check if `keys` are present on the JSON
                
                if method is 'resp_code':
                    NOTE: I just added this, because why not ;)
                    object1: Object containing response code
                    object2: response code to check with object1
    """
    if object1 == object2:
        return True

    if method in ('regex', 're'):
        content, pattern = bytify(object1), bytify(object2)
        if regex.search(pattern, content):  # I now leave everything else to this :p
            return True
        else:
            return False

    elif method in ('headers', 'head', 'header', 'heads'):
        if type(object1) == http_response:
            object1 = object1.headers
        object1 = case_insensative_dict(object1)
        if type(object2) in (list, tuple):
            for key in object2:
                if key not in object1:
                    return False
            return True
        else:
            for key in object2:
                if key in object1:
                    if not match('regex', object1[key], object2[key]):
                        return False
                else:
                    return False
            return True

    elif method == 'json':
        if type(object1) == http_response:
            if object1.headers['Content-Type'] != 'application/json':
                print(warn('WARN -> Response `Content-Type` is not `json`, continuing..'))
            object1 = object1.json()
        elif type(object1) in (str, bytes):
            object1 = json.loads(object1)
        elif isinstance(object, (TextIOBase, BufferedIOBase, RawIOBase, IOBase)):
            object1 = json.load(object1)
        object1 = case_insensative_dict(object1)
        if type(object2) in (list, tuple):
            for key in object2:
                if key not in object1:
                    return False
            return True
        else:
            if type(object2) in (str, bytes):
                object2 = json.loads(object2)
            elif isinstance(object, (TextIOBase, BufferedIOBase, RawIOBase, IOBase)):
                object2 = json.load(object2)
            for key in object2:
                    if key in object1:
                        if not match('regex', object1[key], object2[key]):
                            return False
                    else:
                        return False
            return True

    elif method in ('len', 'length'):
        if type(object2) in (str, bytes):
            if object2.isdigit():
                object2 = b' ' * int(object2)
        elif type(object2) == int:
            object2 = b' ' * object2
        object1, object2 = bytify(object1), bytify(object2)
        cmp1, cmp2 = len(object1), len(object2)

    elif method in ('resp_code', 'status_code', 'response_code'):
        cmp1 = cmp2 = 0
        if type(object1) == http_response:
            object1 = object1.status_code
        cmp1, cmp2 = int(object1), int(object2)
    
    else:
        print(bad('WTH -> UNKNOWN METHOD USED'))


    if cmp1 == cmp2:  # Left comparision from length, response status code
        return True
    else:
        return False


def pad_numbers(face_value, place_value):
    """
    Does padding of numbers,
        like 
            if face_value = 4
            and place_value = 7
            this will return 4000000
        and
            if face_value = 1234567
            and place_value = 4
            this will return 1234
        
        Parameters:
            face_value (int): Face value of a number
            place_value (int): Place value of the number
        
        Returns:
            number (int): Number after padding
    """
    try:
        face_value, place_value = int(face_value), int(place_value)
        if not face_value or not place_value:
            number =  0
        elif len(str(face_value)) < place_value:
            number =  int( str( face_value ) + '0' * (place_value - len( str( face_value ) ) ) )
        else: # len(str(num)) > place_value
            number = int( str ( face_value ) [:place_value] )
        return number
    except ValueError as value_error:
        print(bad('Value Error: {}'.format(value_error)))


def get_max_id(exploit, iid=1, verbose=False):
    """
    I have no idea _what, how, why_ I wrote this but this thing just works, will touch this function later soon as it needs a better implementation.

        Parameters:
            exploit (func): Function that takes `id` as argument, and returns None if -ve response
            iid (int): Stands for initial id to be used
            verbose (bool): Verbosity of the process

        Returns:
            max_id (int): Last / Max / Final `id` of the IDOR
    """
    tries = {}
    permutations = 0
    old_num = num = iid
    place_value = 6
    _ = []
    if not verbose:
        animation = Animate('random', info('Running -> Obtaining max_id'))
        animation.daemon = True
        animation.start()
    while 1:
        permutations += 1
        if num in tries:
            if verbose:
                print('> {} {}'.format(num, tries[num]))
            if tries[num] == 'low':
                old_num = num
                num += pad_numbers(1, place_value)
                _.append(tries[old_num])
            else:
                old_num = num
                num -= pad_numbers(1, place_value)
                _.append(tries[old_num])
            if len(_) >= 2 and len(set(_)) == 1:
                resp1 = exploit(num)
                resp2 = exploit(num + 1)
                if resp1 and not resp2:
                    break
                elif not resp1 and not resp2:
                    resp1 = exploit(num)
                    resp2 = exploit(num - 1)
                    if not resp1 and resp2:
                        num -= 1
                        break
            if len(set(_)) == 2:
                _ = []
                place_value -= 1
            elif len(_) == 2 and len(set(_)) == 1:
                _ = []
        else:
            old_num = num
            resp = exploit(num)
            if resp:
                resp_type = 'low'
                num += pad_numbers(1, place_value)
            else:
                resp_type = 'high'
                num -= pad_numbers(1, place_value)
            _.append(resp_type)
            tries[old_num] = resp_type
            if len(set(_)) == 2:
                _ = []
                place_value -= 1
            elif len(_) == 2 and len(set(_)) == 1:
                _ = []
            if verbose:
                print('- {} {}'.format(num, tries[old_num]))
    if verbose:
        print('{}: {} - {} = {}'.format(num, permutations, len(tries), permutations - len(tries)))
    if not verbose:
        animation.stop()
    clear_line()
    return num


class Exploit(_Thread):
    """
    Used by `dump_all`, just executes an exploit with a range of id using for loop

        Parameters:
            exploit (func): Function/Exploit to be executed against the range of ids
            id_range (list/range/...): Any iterable expecting an id for the function
    """
    def __init__(self, exploit, id_range):
        _Thread.__init__(self)
        self.exploit = exploit
        self.ids = id_range
    
    def run(self):
        global JUICE
        for _id in self.ids:
            juice = self.exploit(_id)
            JUICE[_id] = juice


def dump_all(exploit, min_id, max_id, threads=20, animate=True):
    """
    Dump all the responses from a specific id range

        Parameters:
            exploit (func): Function with an id parameter to be executed
            min_id (int): Initial id to start with
            max_id (int): id to stop iteration on
            threads (int): Number of threads for the function to be executed
            animate (bool): Shall an animation be seen, while the process is running
        
        Returns:
            JUICE (dict): Dictionary with id as key, and response from the function
    """
    # This is now a serious warning, so not commenting it
    print(warn('WARNING -> This action might break CIA Triad based on your agreement..'))
    expected_juice_len = ( ( max_id - min_id ) + 1 ) + len(JUICE)
    if animate:
        animation = Animate('bar', f'Dumping..', expected_juice_len)
        animation.daemon = True
        animation.start()
    _threads = []
    chunks = tuple(chunkify( range(min_id, max_id + 1), threads))
    for chunk in chunks:
        thread = Exploit(exploit, chunk)
        thread.daemon = True
        thread.start()
        _threads.append(thread)
    for thread in _threads:
        thread.join()
    if animate:
        animation.stop()
    return JUICE


def reset_juice():
    """
    Just Empties `JUICE` global variable, which contains response from `dump_all`
    You might want to run this, if you are exploiting different targets from a same script
    """
    global JUICE
    JUICE = {}
