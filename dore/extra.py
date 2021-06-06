
__version__ = 0.001

from .style import *
from os import kill as _kill
from os import getuid as _getuid
from signal import SIGHUP as _SIGHUP
from requests import Response as http_response
from io import TextIOBase, BufferedIOBase, RawIOBase, IOBase
from requests import get as _get
from sys import platform

if platform != 'darwin':
    from sysdmanager import SystemdManager as _sdm
    from psutil import process_iter as _ps
    from dbus.exceptions import DBusException as _DBusException


def proxy_works(proxies, url='https://google.com'):
    """
    Check if a proxy is working, basically tries a GET request to the URL with the proxy

        Parameters:
            proxies (dict): Dictionary consisting of proxies
            url (str): URL to to check with proxy
        
        Returns:
            bool: Boolean, if proxy is working or not
    """
    try:
        _get(
                url,
                proxies=proxies,
                headers={
                            'User-Agent': f'dore/{__version__}'
                        }
            )
    except Exception as err:
        print(bad(f'ERROR -> {err}'))
        return False
    return True


def is_root():
    """
    Returns if user is root or not

        Returns:
            bool: `True` is user is root, else `False`
    """
    if _getuid():
        return False
    return True


def is_active(service_name='tor.service', start=False):
    """
    Returns if a service is active, will start it if asked for

    NOTE: The following function is **NOT** supported with atleast on my WSL..

        Parameters:
            service_name (str): Name of service (eg.: tor.service)
            start (bool): Start if inactive

        Returns:
            bool: Either the service is running or not
    """
    try:
        if not _sdm().is_active(service_name):
            if start:
                _sdm().start_unit(service_name)
                return True
            return False
        return True
    except _DBusException:
        # print(warn('Oops -> WSL not supported for this specific function'))
        pass
    except Exception as err:
        print(bad(f'Error -> {err}'))


def get_pid(process_name='tor'):
    """
    Returns PID of a process

        Parameters:
            process_name (str): Name of process (eg.: tor)

        Returns:
            int: Process ID of queried process name
    """
    try:
        return [p.info for p in _ps(attrs=['pid', 'name']) if p.info['name'] == str(process_name) ][0]['pid']
    except IndexError as index_err:
        print(bad(f'Index Error ({index_err}) -> `{process_name}` not found'))


def renew(method='hup'):
    '''
    Renews TOR IP Address. Make sure, its run by root (uid=0)
    NOTE: Need to add support for other methods, like by using stem maybe, idk..

        Parametes:
            method (str): Method to use for renewing IP Address (eg.: hup)

        Returns:
            bool: If renewal was completed
    '''
    if method.lower() == 'hup':
        if is_root():
            pid = get_pid('tor')
            _kill(pid, _SIGHUP)
            return True
        else:
            print(bad('Make sure you are Super User!'))
    else:
        print(bad('Wait! -> Unknown method'))
    return False


def bytify(object):
    """
    Converts content of given object into bytes-like object

        Parameters:
            object (...): Almost any object (io object, response object, str, json, list...)

        Returns:
            object (bytes): Result bytes-like object
    """
    if type(object) == None:  # Hard-coded None object, for a reason. 
        return None

    elif type(object) == bytes:
        return object

    elif type(object) == http_response:
        object = object.content  # This is always `bytes` object

    elif isinstance(object, (TextIOBase, BufferedIOBase, RawIOBase, IOBase)):
        try:  
            object = bytify(object.read())
        except:
            # Will not interrupt the flow, but might cause a flaw
            object = bytify(str(object))

    else:
        # print(warn('Expected object might not be returned'))
        # If object type is unknown from above categories, THIS MIGHT BE AN ISSUE!
        object = str(object).encode()

    return object


def chunkify(iterable, chunk_length=4):
    """
    Yield chunk_length-sized chunks from an iterable
    
        Parameters:
            iterable: An iterable
            chunk_length: Chunk size for the iterable to be splitted
        
        Retuns:
            iterable: Chunked iterable
    
    Copied from: https://stackoverflow.com/a/312464/190597
    """
    for _ in range(0, len(iterable), chunk_length):
        yield iterable[_:_ + chunk_length]

