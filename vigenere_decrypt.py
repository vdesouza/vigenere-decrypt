import sys


if len(sys.argv) < 2:
    print "Usage: python vigenere_decrypt.py [ciphertext]"
    exit()

# import cipher text
f = open(sys.argv[1], "r")
cipher = f.read()
cipher.rstrip()
f.close()

alpha = "abcdefghijklmnopqrstuvwxyz"

# creates a map of letter frequencies in a text
def generateFrequencies(text):
    ret = {c: 0.0 for c in alpha}
    for c in text:
        if c != '\n':
            ret[c] += 1.0
    return ret

# calculates partial part of the IC
def calc_ic(piece):
    ic_partial = 0.0
    l = float(len(piece))
    freqs = generateFrequencies(piece)
    for char, count in freqs.items():
        ic_partial = ic_partial + ((count / l) * ((count - 1.0) / (l - 1.0)))
    return ic_partial * len(alpha)

english_ic = 1.73
keyword_len = 0
best_ic = 0.0
# try up to keywords of length 20
max_keyword_size = 20
for i in range(1, max_keyword_size + 1):
    pieces = [[] for _ in range(i)]
    for j, c in enumerate(cipher):
        pieces[j % i].append(c)

    ic_sums = 0.0
    for p in pieces:
        ic_sums += calc_ic(p)

    ic = ic_sums / i
    old_ic = best_ic

    # check if best ic found
    if ic < english_ic:
        best_ic = max(old_ic, ic)
    else:
        best_ic = min(old_ic, ic)
    if best_ic != old_ic:
        keyword_len = i

# frequency analysis
cipher_cols = [[] for _ in range(keyword_len)]
for i, c in enumerate(cipher):
    cipher_cols[i % keyword_len].append(c)

cipher_cols_freqs = [generateFrequencies(col) for col in cipher_cols]

# from https://en.wikipedia.org/wiki/Letter_frequency
eng_freqs = [
        0.08167, 0.01492, 0.02782, 0.04253,
        0.12702, 0.02228, 0.02015, 0.06094,
        0.06966, 0.00153, 0.00772, 0.04025,
        0.02406, 0.06749, 0.07507, 0.01929,
        0.00095, 0.05987, 0.06327, 0.09056,
        0.02758, 0.00978, 0.02360, 0.00150,
        0.01974, 0.00074]

# build keyword
keyword = ""
for freq in cipher_cols_freqs:
    shifted_char = 'a'
    max_corr = 0.0
    # find greatest corrolation between column letter fequency and english character frequency
    for char in alpha:
        corr = 0.0
        c = ord(char)
        for k, v in freq.items():
            possible_char = (ord(k) - c + len(alpha)) % len(alpha)
            corr += v * eng_freqs[possible_char]
        if corr > max_corr:
            shifted_char = char
            max_corr = corr
    keyword += shifted_char
keyword_f = open('keyword1.txt', 'w')
keyword_f.write(keyword)
keyword_f.close()

# decrypt using keyword found and cipher
plaintext = []
for idx, char in enumerate(cipher):
    char = chr((ord(char) - ord(keyword[idx % keyword_len]) + len(alpha)) % len(alpha) + ord('a'))
    plaintext.append(char)
message = ''.join(plaintext)
message_f = open('message1.txt', 'w')
message_f.write(message)
message_f.close()
