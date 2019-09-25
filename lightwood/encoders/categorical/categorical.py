import torch
from lightwood.encoders.text.helpers.rnn_helpers import Lang

UNCOMMON_WORD = '<UNCOMMON>'
UNCOMMON_TOKEN = 0

class CategoricalEncoder:

    def __init__(self, is_target = False):
        self._lang = None
        self._pytorch_wrapper = torch.FloatTensor

    def fit(self, priming_data):
        self._lang = Lang('default')
        self._lang.index2word = {UNCOMMON_TOKEN: UNCOMMON_WORD}
        self._lang.word2index = {UNCOMMON_WORD: UNCOMMON_TOKEN}
        self._lang.word2count[UNCOMMON_WORD] = 0
        self._lang.n_words = 1
        for category in column_data:
            if category != None:
                self._lang.addWord(str(category))

    def encode(self, column_data):
        ret = []
        v_len = self._lang.n_words

        for word in column_data:
            encoded_word = [0]*v_len
            if word != None:
                word = str(word)
                index = self._lang.word2index[word] if word in self._lang.word2index else UNCOMMON_TOKEN
                encoded_word[index] = 1

            ret.append(encoded_word)

        return self._pytorch_wrapper(ret)


    def decode(self, encoded_data):

        encoded_data_list = encoded_data.tolist()

        ret = []


        for vector in encoded_data_list:
            found = False


            max_i = 0
            max_val = 0
            for i in range(len(vector)):
                val = vector[i]
                if val > max_val:
                    max_i = i
                    max_val = val
            ret += [self._lang.index2word[max_i]]


        return ret


if __name__ == "__main__":

    data = 'once upon a time there where some tokens'.split(' ') + [None]

    enc = CategoricalEncoder()

    enc.fit(data)

    print(enc.encode(data))

    print(enc.decode(enc.encode(['not there', 'time', 'tokens', None])))
