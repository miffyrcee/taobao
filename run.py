import json
import os
import re
import subprocess
from base64 import urlsafe_b64decode
from multiprocessing import Pool


def decode(obj, reg=''):
    def b64_d(obj):
        try:
            return int(obj)
        except Exception:
            return urlsafe_b64decode(
                '{}=='.format(obj)).decode('utf-8').strip()

    if isinstance(obj, list):
        res = list()
        for oj in obj:
            try:
                oj = b64_d(oj)
            except Exception:
                pass
            res.append(oj)
        obj = res
    else:
        obj = b64_d(obj)

    if reg:
        obj = re.split(reg, obj)
        obj = list(filter(None, obj))
    return obj


def conf_generator():
    fp = os.path.join(os.path.dirname(__file__), 'ssr.txt')
    with open(fp, 'r') as fr:
        obj = fr.read()
    obj = decode(obj, r'\n|ssr:\/\/|\n|ss:\/\/')
    obj = [decode(parm, r'\/\?|:|=|&') for parm in obj]
    obj = [decode(parm) for parm in obj]
    return obj


def ping(label, single_conf):
    res = subprocess.call('tcping -t 1 {} {}'.format(
        single_conf[0], single_conf[1]).split(' '),
        stdout=subprocess.PIPE)
    if res == 0:
        res = 'open'
    else:
        res = 'close'
    print(label, single_conf[-3], '¦', res)


def ping_show(conf_list, ping_test=True):
    if not ping_test:
        for lable, single_conf in enumerate(conf_list):
            print(lable, single_conf[-3])
        return
    pool = Pool(processes=4)
    res = [
        pool.apply_async(ping, (label, single_conf))
        for label, single_conf in enumerate(conf_list)
    ]
    [r.get(timeout=30) for r in res]


def setting_generator(conf, label):
    single_conf = conf[label]

    def intersection(value):
        try:
            return set(value).intersection(set(single_conf)).pop()
        except Exception:
            return ''

    fp = os.path.join(os.path.dirname(__file__), 'ssr_config.json')
    with open(fp, 'r') as fr:
        obj = json.loads(fr.read())

    setting = obj
    setting['server'] = single_conf[0]
    setting['server_port'] = single_conf[1]
    setting['password'] = single_conf[5]
    setting['method'] = intersection(obj['method'])
    setting['obfs'] = intersection(obj['obfs'])
    setting['obfs_param'] = intersection(obj['obfs_param'])
    setting['protocol'] = intersection(obj['protocol'])
    setting['protocol_param'] = intersection(obj['protocol_param'])
    return setting


def sync_conf(conf):
    label = int(input('number: '))
    print(setting_generator(conf, label))
    label_enter = int(input('Enter: '))
    if label_enter:
        fd = os.path.abspath('/etc/shadowsocksr/ssr-local.json')
        with open(fd, 'w') as fp:
            fp.write(json.dumps(setting_generator(conf, label)))
        subprocess.call('sudo systemctl restart ssr-local'.split(' '))


if __name__ == "__main__":
    ping_show(conf_generator(), True)
    sync_conf(conf_generator())
