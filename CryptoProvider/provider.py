## web
from flask import Flask, request

## homomorphic encryption
import nufhe
from phe import paillier
from utils import EncUInt8

class CryptoProvider(object):
    def __init__(self, device_id):
        self.session = self._create_session(device_id)

    def _generate_fhe_keys(self, ctx):
        secret_key, cloud_key = ctx.make_key_pair()

        return secret_key, cloud_key

    def _create_session(self, device_id):
        devices = nufhe.find_devices(api="OpenCL")
        ctx = nufhe.Context(device_id=devices[device_id])

        fhe_sk, fhe_pk = self._generate_fhe_keys(ctx)
        phe_sk, phe_pk = self._generate_phe_keys()

        session = {
            'ctx' : ctx,
            'private_keys': {
                'fhe_sk' : fhe_sk,
                'phe_sk' : phe_sk
            },
            'public_keys' : {
                'phe_pk' : phe_sk,
                'fhe_pk' : fhe_pk
            }
        }

        return session
    
    def _generate_phe_keys(self):
        public_key, private_key = paillier.generate_paillier_keypair()

        return public_key, private_key

    def _reencrypt_phe_to_fhe():
        pass

    def make_web_controller(self):
        crypto_provider_ctrl = Flask("crypto-provider")

        @crypto_provider_ctrl.route('/phe_public_key', methods=['GET'])
        def phe_public_key():
            public_key = self.session['public_keys']['phe_pk']
            return str(public_key.n)

        @crypto_provider_ctrl.route('/fhe_public_key', methods=['GET'])
        def fhe_public_key():
            public_key = self.session['public_keys']['fhe_pk']
            return public_key.dumps()

        @crypto_provider_ctrl.route('/reencrypt', methods=['POST'])
        def reencrypt():
            request_json = request.json
            x = request_json['value']

            phe_sk = self.session['private_keys']['phe_sk']
            phe_pk = self.session['public_keys']['phe_pk']

            enc_value = paillier.EncryptedNumber(phe_pk, int(x), 0)
            value = phe_sk.decrypt(enc_value)

            fhe_sk = self.session['private_keys']['fhe_sk']
            fhe_pk = self.session['public_keys']['fhe_pk']
            ctx = self.session['ctx']
            vm = ctx.make_virtual_machine(fhe_pk)
            
            fhe_value = EncUInt8.from_uint8(vm, fhe_sk, ctx, value)

            return fhe_value.dumps()

        return crypto_provider_ctrl

if __name__ == "__main__":
    provider = CryptoProvider(device_id=1)
    web_controller = provider.make_web_controller()
    web_controller.run()