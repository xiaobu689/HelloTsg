import rsa
import json
import hashlib
import time
import random
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def get_uuid(length=36):
    chars = "0123456789abcdef"
    uuid_list = [random.choice(chars) for _ in range(length)]

    # Set the UUID version (4)
    uuid_list[14] = '4'

    # Set the UUID variant (8, 9, a, or b)
    uuid_list[19] = chars[(int(uuid_list[19], 16) & 0x3) | 0x8]

    # Set the fixed UUID format
    uuid_format = [8, 13, 18, 23]
    for i in uuid_format:
        uuid_list[i] = '-'

    # Join the list into a string
    uuid_str = ''.join(uuid_list)
    print("---------------------uuid_str=",uuid_str)

    return uuid_str

def generate_aes_key():
    return get_random_bytes(16)

def encrypt_aes_key(aes_key, rsa_pub_key):
    return rsa.encrypt(aes_key, rsa_pub_key)

def aes_encrypt(data, aes_key):
    cipher = AES.new(aes_key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return b64encode(encrypted_data).decode('utf-8')

# 获取当前环境
environment = "dev"  # 或者 "test", "prod" 取决于你的环境

# 配置
config = {
    "dev": {
        "rsakey": """
            -----BEGIN PUBLIC KEY-----
            MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCwiEnCkRR9cEZPWbDcr6/hTASOZSUyMQ2Ghm2eCxqtFpDrUAnfH6PDjcPjjCFAO4HdOsqetOu7fq9cLXMSunVdYLewQdl/0UD+0BARGGeGl3oxnjwvGSWDo8D/eWxE7m1AIuRu9/qTH5A8WtuvR6bTnEbh2ZaU9NzUC911O8MXkQIDAQAB
            -----END PUBLIC KEY-----
        """,
        "rsasecret": "JXetbk3ITipFrbeMDFcP"
    },
    "test": {
        "rsakey": """
            -----BEGIN PUBLIC KEY-----
            MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCQQ0sOToNuhKmJafplhWzzfMHrivyvurDL9Fc02VKIbIUts7hD4AyR1oPnz25a3DBDca5ANTrW0CYxL5wDMbvN115cEEQ8wH9HdX5KNADDR8BD5ozzoj7p35pzo2//Ncn5/o/R9Lc7e+hdJZjYBt8lBzaRm0FVcfIza/V0/0DDuQIDAQAB
            -----END PUBLIC KEY-----
        """,
        "rsasecret": "OUiLREBIJqWzaXQYQ6Rr"
    },
    "prod": {
        "rsakey": """
            -----BEGIN PUBLIC KEY-----
            MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCBbNpsLhjS/Kq2JrG6DwzgO22OtwjX3sxazFHn8p9cfKV0rqnWmV4CG3D0yDN9I2VFGahkeLaCdBRV3XjvXCtmjN0/ragbIvjhRibYPmXr2Tyfy6mJG2fcjwK7E1v3drWo+wGt0LpPGz2oKtndZq3gh4UUZkGWH6x1r7H4pCwRMQIDAQAB
            -----END PUBLIC KEY-----
        """,
        "rsasecret": "Ww2sbzP4rjRNmQAmkjuj"
    }
}

# 选择当前环境的配置
current_config = config[environment]

# 构造数据
data = {
    "outOrderNo": get_uuid(),
    "mobile": "17854279565",  # 替换成你的具体数据
    "timestamp": str(int(time.time())),
    "sysId": "T0000001",
    "channelId": "APP",
    "token": "wx.getStorageSync('token')"  # 替换成你的具体数据
}

# 按照 JavaScript 代码逻辑生成排序后的键值对字符串
sorted_items = []
for key in sorted(data):
    value = data[key]
    if isinstance(value, dict) or isinstance(value, list):
        value = json.dumps(value, separators=(',', ':'))
    sorted_items.append(f"{key}={value}")

# 使用 MD5 算法计算签名
sign_string = '&'.join(sorted_items)
sign_md5 = hashlib.md5(sign_string.encode()).hexdigest()

# 添加签名到数据中
data['sign'] = sign_md5

# 序列化为 JSON
json_data = json.dumps(data, separators=(',', ':'))

# 生成 AES 密钥并加密数据
aes_key = generate_aes_key()
encrypted_data = aes_encrypt(json_data, aes_key)

# 加密 AES 密钥
pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(current_config['rsakey'].encode('utf-8'))
encrypted_aes_key = encrypt_aes_key(aes_key, pub_key)

# Base64 编码加密后的数据和加密后的 AES 密钥
dataVerify = encrypted_data
encryptedAESKey = b64encode(encrypted_aes_key).decode('utf-8')

print(f"dataVerify: '{dataVerify}'")
print(f"encryptedAESKey: '{encryptedAESKey}'")
