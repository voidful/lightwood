import torch
from lightwood.encoders.text.helpers.rnn_helpers import Lang

UNCOMMON_WORD = '<UNCOMMON>'
UNCOMMON_TOKEN = 0

class CategoricalEncoder:

    def __init__(self):

        self._lang = None

    def encode(self, column_data):

        if self._lang is None:
            self._lang = Lang('default')
            self._lang.index2word =  {UNCOMMON_TOKEN: UNCOMMON_WORD}
            self._lang.n_words = 1
            for word in column_data:
                if word != None:
                    self._lang.addWord(word)

        ret = []
        v_len = self._lang.n_words

        for word in column_data:
            encoded_word = [0]*v_len
            if word != None:
                index = self._lang.word2index[word] if word in self._lang.word2index else UNCOMMON_TOKEN
                encoded_word[index] = 1

            ret += [encoded_word]

        return torch.FloatTensor(ret)


    def decode(self, encoded_data):

        encoded_data_list = encoded_data.tolist()

        ret = []


        for vector in encoded_data_list:
            found = False
            for i, val in enumerate(vector):
                if int(val) == 1:
                    found = True
                    ret += [self._lang.index2word[i]]
                    break
            if not found:
                ret += [None]

        return ret


if __name__ == "__main__":

    data = 'once upon a time there where some tokens'.split(' ') + [None]

    enc = CategoricalEncoder()

    print (enc.encode(data))

    print(enc.decode(enc.encode(['not there', 'time', 'tokens', None])))


