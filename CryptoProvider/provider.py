## web
from flask import Flask, make_response, request
import json
import base64
import pickle

## homomorphic encryption
import nufhe
from phe import paillier
from utils import EncUInt8

class CryptoProvider(object):
    def __init__(self, device_id):
        self.session = self._create_session(device_id)

    def _generate_fhe_keys(self, ctx):
        secret_key, cloud_key = ctx.make_key_pair()

        with open('fhe_keys.pickle', 'wb') as f:
            pickle.dump([secret_key.dumps(), cloud_key.dumps()], f)

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
                'phe_pk' : phe_pk,
                'fhe_pk' : fhe_pk
            }
        }

        return session
    
    def _generate_phe_keys(self):
        public_key, private_key = paillier.generate_paillier_keypair()

        with open('phe_keys.pickle', 'wb') as f:
            pickle.dump([public_key, private_key], f)

        return private_key, public_key

    def _reencrypt_phe_to_fhe(self, values_cipher):
        phe_sk = self.session['private_keys']['phe_sk']
        phe_pk = self.session['public_keys']['phe_pk']

        values_enc = [paillier.EncryptedNumber(phe_pk, int(x), 0) for x in values_cipher]
        values = [phe_sk.decrypt(x) for x in values_enc]

        fhe_sk = self.session['private_keys']['fhe_sk']
        fhe_pk = self.session['public_keys']['fhe_pk']
        ctx = self.session['ctx']
        vm = ctx.make_virtual_machine(fhe_pk)
        
        fhe_values = [EncUInt8.from_uint8(vm, fhe_sk, ctx, x) for x in values]

        return fhe_values

    def make_web_controller(self):
        crypto_provider_ctrl = Flask("crypto-provider")

        # @crypto_provider_ctrl.after_request
        # def add_header(response):
        #     response.headers['Access-Control-Allow-Origin'] = '*'
        #     response.headers['content-type'] = 'application/json'
        #     return response

        def set_header(resp):
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['content-type'] = 'application/json'

            return resp

        @crypto_provider_ctrl.route('/phe_public_key', methods=['GET'])
        def phe_public_key():
            public_key = self.session['public_keys']['phe_pk']
            resp = make_response(json.dumps({ 'phe_pk' : str(public_key.n) }))

            return set_header(resp)

        @crypto_provider_ctrl.route('/fhe_public_key', methods=['GET'])
        def fhe_public_key():
            public_key = self.session['public_keys']['fhe_pk']
            data = base64.b64encode(public_key.dumps()).decode('utf-8')
            resp = make_response(json.dumps({ 'fhe_pk' : data }))

            return set_header(resp)

        @crypto_provider_ctrl.route('/decrypt', methods=['POST'])
        def decrypt():
            fhe_sk = self.session['private_keys']['fhe_sk']
            fhe_pk = self.session['public_keys']['fhe_pk']

            ctx = self.session['ctx']
            vm = ctx.make_virtual_machine(fhe_pk)

            values_cipher = request.json
            values_fhe = [base64.b64decode(x.encode('utf-8')) for x in values_cipher]
            values_fhe = [EncUInt8.from_ciphertext(vm, ctx, x) for x in values_fhe]
            values = [int(x.decrypt(fhe_sk, ctx)[0]) for x in values_fhe]

            resp = make_response(json.dumps(values))
            return set_header(resp)

        @crypto_provider_ctrl.route('/reencrypt', methods=['POST'])
        def reencrypt():
            values_cipher = request.json            
            fhe_values = self._reencrypt_phe_to_fhe(values_cipher)
            data = [base64.b64encode(x.dumps()).decode('utf-8') for x in fhe_values]

            resp = make_response(json.dumps(data))
            return set_header(resp)

        return crypto_provider_ctrl

if __name__ == "__main__":
    provider = CryptoProvider(device_id=1)
    web_controller = provider.make_web_controller()
    web_controller.run()