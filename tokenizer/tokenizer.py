# ---------------------------------------------------------------------------------------------------------------------------------------

from tokenizer.base import countf, mergef, BaseTokenizer

class BytePairEncoding(BaseTokenizer):

    def __init__(self, pattern):

        self.string = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""" if pattern is None else pattern

        self.tokens = dict({i: bytes([i]) for i in range(256)});

        self.merges = dict()

    def training(self, corpora, volumen):

        encode = list(list(i.encode("utf-8")) for i in self.tokenf(corpora)); volumen -= 256

        tokens = dict({i: bytes([i]) for i in range(256)})

        merges = dict()

        from functools import partial

        for i in range(volumen):

            couple = countf(encode); couple = max(couple, key = couple.get)

            decode = tokens[couple[0]] + tokens[couple[1]]
            
            number = i + 256

            pfunct = partial(mergef, couple, number)

            for k in range(len(encode)):

                encode[k] = pfunct(encode[k])

            merges.update({couple: number})

            tokens.update({number: decode})

        self.merges = merges

        self.tokens = tokens
        
# ---------------------------------------------------------------------------------------------------------------------------------------