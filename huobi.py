#coding=utf-8
import time, re, requests, md5, urllib, urllib2, json

URL = 'https://api.huobi.com/api.php'
def get_depth(currency='BTC', timeout=3):
    if currency == 'BTC':
        url = 'http://market.huobi.com/staticmarket/detail.html'
        resp = requests.get(url, timeout=timeout)   
        return  json.loads(re.search('view_detail\((.+)\)', resp.text).group(1))

class HuoBi(object):
    def __init__(self, access_key, secret_key, request_timeout=3):
        self.exchange = 'HUOBI'
        self.access_key = access_key
        self.secret_key = secret_key
        self.request_timeout = request_timeout

    def _sign(self, params):
        params = '&'.join(sorted(["%s=%s"%(k, v) for k, v in params.items()]))
        #print 's:',s
        return md5.new(params).hexdigest().lower()

    def _request(self, params):
        params['access_key'] = self.access_key
        params['secret_key'] = self.secret_key
        params['created'] = str(int(time.time()))
        sign = self._sign(params)
        params['sign'] = sign
        #print params
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        r = requests.post(URL, data=params, headers=headers, timeout=self.request_timeout)
        return r.json()

    def get_account_info(self):
        params = {'method': 'get_account_info'}
        return self._request(params)

    def buy(self, price, amount, currency='BTC'):
        params = {'method': 'buy',
                  'price': price,
                  'amount': amount}
        return self._request(params)

    def sell(self, price, amount, currency='BTC'):
        params = {'method': 'sell',
                  'price': price,
                  'amount': amount}
        return self._request(params)
    
    def cancel_order(self, order_id, currency='BTC'):
        params = {'method':'cancel_delegation',
                  'id':order_id}
        return self._request(params)

    def get_depth(self, currency, timeout=None):
        if not timeout:
            timeout = self.request_timeout
        return get_depth(currency, timeout)
    
    def get_order(self, order_id, currency='BTC'):
        params = {'method':'delegation_info',
                  'id':order_id}
        return self._request(params)
