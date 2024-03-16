import json
import time
import hashlib
import hmac
import base64
import uuid
import requests


class SwitchBot:
    """
    SwitchBot APIを利用するためのクラス
    Args:
        token (str): SwitchBot APIのトークン
        secret (str): SwitchBot APIのシークレット
    """

    def __init__(self, token: str, secret: str):
        self.token = token
        self.secret = secret
        self.base_url = 'https://api.switch-bot.com/v1.1/'

    """
    リクエストヘッダーのための署名を作成する
    Args:
        None
    Returns:
        sign (str): 署名
        t (str): タイムスタンプ
        nonce (str): ランダムな文字列
    """

    def make_sign(self):
        nonce = str(uuid.uuid4())
        t = int(round(time.time() * 1000))
        string_to_sign = f"{self.token}{t}{nonce}".encode('utf-8')
        secret = self.secret.encode('utf-8')
        sign = base64.b64encode(hmac.new(secret, string_to_sign, digestmod=hashlib.sha256).digest())    # NOQA
        return sign, str(t), nonce

    def make_headers(self):
        sign, t, nonce = self.make_sign()
        headers = {
            'Authorization': self.token,
            'sign': sign,
            't': t,
            'nonce': nonce
        }
        return headers

    """
    デバイスの一覧を取得し、JSONファイルに保存する
    Args:
        None
    Returns:
        None
    """

    def get_device_list(self):
        url = self.base_url + 'devices'
        headers = self.make_headers()

        try:
            responce = requests.get(url, headers=headers)
            responce.raise_for_status()  # httpステータスが200番台でない場合は例外を発生させる

            print(responce.text)
            device_list = json.loads(responce.text)
            with open('device_list.json', 'w', encoding='utf-8') as f:
                json.dump(device_list, f, ensure_ascii=False, indent=2)

        except requests.exceptions.RequestException as e:
            print(f"Responce Error : {e}")
