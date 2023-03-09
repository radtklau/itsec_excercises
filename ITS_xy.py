#from Crypto.Cipher import AES
#from base64 import b64encode, b64decode

#cipher_text = "ea3ced4d2a786e6b68b349f717dd0fc9"
#iv = "3b8044b0a048a87a27e4f1aedc5bf52d"

def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

iv_bin = "00111011100000000100010010110000101000000100100010101000011110100010011111100100111100011010111011011100010110111111010100101101"
iv_bin_arr = []

for i in range(len(iv_bin)):
    iv_bin_arr.append(int(iv_bin[i]))

text = "run,we're blown."
malicious_text = "meet you tonight"
xor1 = []
xor2 = []
text_bin = tobits(text)
malicious_text_bin = tobits(malicious_text)

for i in range(len(text_bin)):
    xor1.append(text_bin[i] ^ malicious_text_bin[i])

for i in range(len(iv_bin_arr)):
    xor2.append(xor1[i] ^ iv_bin_arr[i])

malicious_iv = ""

for i in range(len(xor2)):
    malicious_iv = malicious_iv+str(xor2[i])

print("internet method")
print(hex(int(malicious_iv, 2)))
print("----")

#if recipitent decodes message with this IV the text is altered to "meet you tonight"

iv_bin = "00111011100000000100010010110000101000000100100010101000011110100010011111100100111100011010111011011100010110111111010100101101"
text_bin = "01110010011101010110111000101100011101110110010100100111011100100110010100100000011000100110110001101111011101110110111000101110"
malicious_text_bin = "01101101011001010110010101110100001000000111100101101111011101010010000001110100011011110110111001101001011001110110100001110100"
malicious_iv_bin = ""
decrypted = ""
#first method
for i in range(len(iv_bin)):
    decrypted = decrypted+str(int(iv_bin[i]) ^ int(text_bin[i]))
#print("decrypted "+decrypted)

mivb2 = ""

for i in range(len(iv_bin)):
    if decrypted[i] == malicious_text_bin[i]:
        mivb2 = mivb2+"0" #dont change decrypted
    else:
        mivb2 = mivb2+"1" #change decrypted
#

#second method
for i in range(len(iv_bin)):
    if text_bin[i] != malicious_text_bin[i]:
        if iv_bin[i] == "0":
            malicious_iv_bin = malicious_iv_bin+"1"
        else:
            malicious_iv_bin = malicious_iv_bin+"0"
        continue
    malicious_iv_bin = malicious_iv_bin+iv_bin[i]
#

print("first method")
print(mivb2)
print(hex(int(mivb2, 2)))
print("----")
print("second method")
print(malicious_iv_bin)
print(hex(int(malicious_iv_bin, 2)))
print("----")



