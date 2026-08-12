"""Check Alibaba Cloud DNS records for miaoshoutang.icu"""
import sys, os, hashlib, hmac, base64, urllib.request, urllib.parse, json, uuid
from datetime import datetime, timezone

def percent_encode(s):
    if isinstance(s, str): s = s.encode('utf-8')
    res = []
    for byte in s:
        if (0x30 <= byte <= 0x39 or 0x41 <= byte <= 0x5A or 0x61 <= byte <= 0x7A or byte in (0x2D, 0x2E, 0x5F, 0x7E)):
            res.append(chr(byte))
        else:
            res.append(f'%{byte:02X}')
    return ''.join(res)

def sign(method, params, secret):
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    canonicalized = '&'.join(f'{percent_encode(k)}={percent_encode(str(v))}' for k, v in sorted_params)
    string_to_sign = f'{method}&{percent_encode("/")}&{percent_encode(canonicalized)}'
    key = (secret + '&').encode('utf-8')
    signature = hmac.new(key, string_to_sign.encode('utf-8'), hashlib.sha1)
    return base64.b64encode(signature.digest()).decode('utf-8')

def get_records(access_id, access_secret, domain):
    now = datetime.now(timezone.utc)
    params = {
        'Format': 'JSON',
        'Version': '2015-01-09',
        'AccessKeyId': access_id,
        'SignatureMethod': 'HMAC-SHA1',
        'Timestamp': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'SignatureVersion': '1.0',
        'SignatureNonce': str(uuid.uuid4()),
        'Action': 'DescribeDomainRecords',
        'DomainName': domain,
    }
    sig = sign('GET', params, access_secret)
    params['Signature'] = sig
    qs = urllib.parse.urlencode(params)
    url = f'https://alidns.aliyuncs.com/?{qs}'
    req = urllib.request.Request(url)
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        data = json.loads(resp.read().decode())
        return data.get('DomainRecords', {}).get('Record', [])
    except Exception as e:
        print(f'Error: {e}')
        return []

if __name__ == '__main__':
    # Read credentials from env vars or a config file
    access_id = os.getenv('ALIBABA_ACCESS_KEY_ID')
    access_secret = os.getenv('ALIBABA_ACCESS_KEY_SECRET')

    # Try to read from a non-gitignored config
    cfg_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.aliyun_creds')
    if (not access_id or not access_secret) and os.path.exists(cfg_file):
        with open(cfg_file) as f:
            lines = f.read().strip().split('\n')
            if len(lines) >= 2:
                access_id = lines[0].strip()
                access_secret = lines[1].strip()

    if not access_id or not access_secret:
        access_id = input('AccessKey ID: ').strip()
        access_secret = input('AccessKey Secret: ').strip()

    domain = 'xn--cksv0b2zp.icu'
    print(f'Querying DNS records for: {domain}')
    print(f'{"Type":10s} {"RR":15s} {"Value":45s} Status')
    print('-' * 80)

    records = get_records(access_id, access_secret, domain)
    for r in records:
        print(f'{r["Type"]:10s} {r["RR"]:15s} {r["Value"]:45s} {r.get("Status","?")}')

    if not records:
        print('(No records found)')
