import random
from pathlib import Path



def get_random_proxy():
    p  = Path('..')

    proxy_list_path=list(p.glob('**/proxy_list.txt'))[0].resolve()

    with open(proxy_list_path) as f:
        proxies=f.readlines()
    proxy_ip = random.choice(proxies).strip().split(':')[0]
    print('****random proxy assigned*****')
    return proxy_ip   