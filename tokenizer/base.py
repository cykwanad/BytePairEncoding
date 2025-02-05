# ---------------------------------------------------------------------------------------------------------------------------------------

def mergef(couple, number, encode):

    # Given a list of integers, replace all consecutive occurrences of pair with the new integer
    
    # ((1, 2), 4, [1, 2, 3, 1, 2]) → ([4, 3, 4])
    
    for i in range(len(encode[1:])):

        if tuple(encode[i:i+2]) == couple:

            encode[i] = number; encode[i+1:] = mergef(couple, number, encode[i+2:])

            break

    return encode

def countf(encode):

    # Given a list of integers, return a dictionary of counts of consecutive pairs

    # ([1, 2, 3, 1, 2, 1, 2]) → {(1, 2): 3, (2, 3): 1, (3, 1): 1, (2, 1): 1})
        
    counts = list(k for i in encode for k in zip(i[0:], i[1:]))

    import collections

    return dict(collections.Counter(counts))

# ---------------------------------------------------------------------------------------------------------------------------------------

class BaseTokenizer:

    def encode(self, corpora):

        chunks = self.tokenf(corpora); encode = list()

        for i in chunks:

            target = list(i.encode("utf-8"))

            while len(target) > 1:

                couple = min(countf([target]), key = lambda i: self.merges.get(i, float("inf")))
                
                if couple not in self.merges:

                    break
                
                number = self.merges.get(couple)
                
                target = mergef(couple, number, target)

            encode.extend(target)

        return encode
    
    def decode(self, indexes):
    
        decode = list((self.tokens[i]).decode("utf-8") for i in indexes)

        return decode[0]
    
    def access(self, pointer):

        with open(pointer, chr(114)) as file:

            self.merges = dict(); self.string = file.readline().strip()
            
            self.tokens = dict(); number = 256
            
            for i in file:

                self.merges[tuple(map(int, i.split()))] = number

                number += 1

        self.tokens = self.vocabs()

    def export(self, pointer):

        with open(pointer, chr(119)) as file:
        
            file.write(f"{self.string}\n")

            for i in self.merges:

                file.write(f"{i[0]} {i[1]}\n")

    def vocabs(self):

        tokens = dict({i: bytes([i]) for i in range(256)})

        for i in self.merges.items():

            decode = tokens[i[0][0]] + tokens[i[0][1]]

            tokens[i[1]] = decode

        return tokens

    def tokenf(self, corpora):

        from regex import findall as match
        
        return match(self.string, corpora)

# ---------------------------------------------------------------------------------------------------------------------------------------