## web
from flask import Flask, make_response, request
import requests as http
import base64
import json

## homomorphic encryption
import nufhe
from phe import paillier
from utils import EncUInt8, sort_encrypted

import numpy as np
import pickle

class BulletinBoard(object):
    def __init__(self, size, provider_uri, ctx):
        self.votes_enc = np.zeros(size, dtype=np.uint8)
        self.provider_uri = provider_uri
        self.size = size
        
        self.ctx = ctx

        self.phe_pk, self.fhe_pk = self._get_public_keys()
        self.vm = self.ctx.make_virtual_machine(self.fhe_pk)

    def _add_noise(self, votes):
        noise = np.random.randint(1, 128, self.size)

        return votes + noise, noise

    def _remove_noise(self, votes_noisy, noise):
        noise_cipher = [EncUInt8.from_scalar(self.vm, x - 1) for x in noise]
        noise_cipher = np.array(noise_cipher)

        votes_fhe = votes_noisy - noise_cipher

        return votes_fhe

    def _sort(self, votes_fhe):
        indecies = [EncUInt8.from_scalar(self.vm, x) for x in range(self.size)]

        print (type(indecies[0]))
        print (type(votes_fhe[0]))

        cipher_to_idx = {}
        for i in range(self.size):
            cipher_to_idx[indecies[i].dumps()] = i

        sort_encrypted(votes_fhe, indecies, self.vm)

        ## add noise
        # indecies_noisy, noise = self._add_noise(indecies)

        indecies_cipher = [base64.b64encode(x.dumps()).decode('utf-8') for x in indecies]
        body = json.dumps(indecies_cipher)

        headers = {'content-type': 'application/json'}
        resp = http.post(self.provider_uri + '/decrypt', data=body, headers=headers)
        result = resp.json()
        print (result)

        return result

    def _get_public_keys(self):
        ## http requests
        # headers = {'content-type': 'application/json'}

        ## phe
        res = http.get(self.provider_uri + '/phe_public_key')
        phe_n = res.json()['phe_pk']

        ## fhe
        res = http.get(self.provider_uri + '/fhe_public_key')
        fhe_b64 = res.json()['fhe_pk']
        fhe_bytes = base64.b64decode(fhe_b64.encode('utf-8'))
        # fhe_bytes_json = fhe_bytes_json.encode('utf-8')

        fhe_pk = self.ctx.load_cloud_key(fhe_bytes)
        phe_pk = paillier.PaillierPublicKey(n=int(phe_n))

        return phe_pk, fhe_pk

    def _reencrypt_votes(self):
        votes_noisy, noise = self._add_noise(self.votes_enc)

        votes_cipher = [str(x.ciphertext()) for x in votes_noisy]
        body = json.dumps(votes_cipher)

        headers = {'content-type': 'application/json'}
        resp = http.post(self.provider_uri + '/reencrypt', data=body, headers=headers)
        votes_noisy_fhe_b64 = resp.json()

        votes_noisy_fhe_bytes = [base64.b64decode(x.encode('utf-8')) for x in votes_noisy_fhe_b64]
        votes_noisy_fhe = [EncUInt8.from_ciphertext(self.vm, self.ctx, x) for x in votes_noisy_fhe_bytes]
        votes_noisy_fhe = np.array(votes_noisy_fhe)
        
        votes_fhe = self._remove_noise(votes_noisy_fhe, noise)

        return votes_fhe

    def make_web_controller(self):
        bulletin_board_ctrl = Flask("bulletin-board")

        def set_header(resp):
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['content-type'] = 'application/json'

            return resp

        @bulletin_board_ctrl.route('/phe_votes', methods=['POST'])
        def get_phe_votes():
            data = request.json
            votes = [paillier.EncryptedNumber(self.phe_pk, int(x), 0) for x in data]
            votes = np.array(votes)
            self.votes_enc = votes + self.votes_enc

            return ''

        @bulletin_board_ctrl.route('/sorted_votes', methods=['GET'])
        def sorted_votes():
            # votes_cipher = [str(x.ciphertext()) for x in self.votes_enc]
            # data = json.dumps(votes_cipher)

            votes_fhe = self._reencrypt_votes()
            result = self._sort(votes_fhe)

            # print (result)

            # data = [base64.b64encode(x.dumps()).decode('utf-8') for x in votes_fhe]

            resp = make_response(json.dumps(result))
            return set_header(resp)

        return bulletin_board_ctrl