import os
import json
from scipy.spatial.distance import cosine

class Encoder:

    def __init__(self):

        self.encoder_path = os.path.join(os.getcwd(), 'encoder.json')
        self.encoder_data = json.loads(open(self.encoder_path).read())

    
    def encode(self, text):

        pairs = str(text).split()
        codes = []

        for pair in pairs:

            code = ""

            for char in pair:

                code += str(self.encoder_data[char])

            code = int(code)
            codes.append(code)


        return codes
    

    def similarity(self, first, second):

        first = self.encode(first)
        second = self.encode(second)

        value = cosine(first, second)

        return value
