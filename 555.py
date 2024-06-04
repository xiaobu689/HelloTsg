import hashlib
import time


class SignatureGenerator:
    def __init__(self):
        self.D = ""
        self.p = 0
        self.E = 0

    def get_signature(self, *args):
        y = int(time.time() * 1000)  # 获取当前时间戳（毫秒）

        if self.D and self.p and self.E > y:
            C = self.D + "apyuc3#7%m4*"
        else:
            try:
                # 假设这里获取了用户密钥 g
                g = self.get_user_crypto_key()
                self.E = g["expireTime"]
                self.p = g["version"]
                self.D = g["encryptKey"]
                C = self.D + "apyuc3#7%m4*"
            except Exception as e:
                print("Error getting user crypto key:", str(e))
                return None

        if args:
            C += "".join(args)

        signature = hashlib.sha256(C.encode()).hexdigest()
        return {
            "signature": signature,
            "version": self.p,
            "expireTime": self.E
        }

    def get_user_crypto_key(self):
        # 假设这里从某个地方获取用户密钥
        # 返回一个包含版本号、过期时间和加密密钥的字典
        return {
            "version": 123,
            "expireTime": int(time.time() * 1000) + 3600000,  # 1小时后过期
            "encryptKey": "some_secret_key"
        }


# 示例用法
generator = SignatureGenerator()
result = generator.get_signature("additional", "data")
print(result)
