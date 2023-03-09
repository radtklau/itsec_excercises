#28 b4 3e 63 17 c3 a1 5d f5 09 68 26 50 4f dc a9 f2 1c a9 c3 e5 5e 89 1c ae 72 aa 1e 75 a9 07 46 2f dc 24 d0 be 21 b4 71 a1 2f 29 c8 13 a5 7f 41 cc 94 6b e4 1b 66 ad 10 4b 16 0f 23 06 46 dd db

#4 blocks
#1: 28 b4 3e 63 17 c3 a1 5d f5 09 68 26 50 4f dc a9
#2: f2 1c a9 c3 e5 5e 89 1c ae 72 aa 1e 75 a9 07 46
#3: 2f dc 24 d0 be 21 b4 71 a1 2f 29 c8 13 a5 7f 41
#4: cc 94 6b e4 1b 66 ad 10 4b 16 0f 23 06 46 dd db

import base64
import subprocess

if __name__ == "__main__":

    cipher = "KLQ+YxfDoV31CWgmUE/cqfIcqcPlXokcrnKqHnWpB0Yv3CTQviG0caEvKcgTpX9BzJRr5BtmrRBLFg8jBkbd2w==" #cipher
    cipher_hex = base64.b64decode(cipher) #base64 decode cipher

    c_old_block1 = bytearray(cipher_hex[:16]) #partition cipher in blocks
    c_old_block2 = bytearray(cipher_hex[16:32])
    c_old_block3 = bytearray(cipher_hex[32:48])
    c_old_block4 = bytearray(cipher_hex[48:])
    c_old_blocks = [c_old_block1,c_old_block2,c_old_block3,c_old_block4]

    c_new_block1 = bytearray(16) 
    c_new_block2 = bytearray(16)
    c_new_block3 = bytearray(16)
    c_new_block4 = bytearray(16)
    c_new_blocks = [c_new_block1,c_new_block2,c_new_block3,c_new_block4]
  
    p_old = "Oh, nice, it works faster than I had expected." #48 byte
    p_new = "'); DROP TABLE Laurids;-- not the data you need" #47 byte -> 1 byte padding needed
    p_old_encoded = p_old.encode('utf-8')
    p_new_encoded = p_new.encode('utf-8')

    p_old_block1 = bytearray(p_old_encoded[:16])
    p_old_block2 = bytearray(p_old_encoded[16:32])
    p_old_block3 = bytearray(p_old_encoded[32:])
    p_old_blocks = [p_old_block1,p_old_block2,p_old_block3]

    p_new_block1 = bytearray(p_new_encoded[:16]) 
    p_new_block2 = bytearray(p_new_encoded[16:32])
    p_new_block3 = bytearray(p_new_encoded[32:])
    p_new_blocks = [p_new_block1,p_new_block2,p_new_block3]


    i_old_block1 = bytearray(16) 
    i_old_block2 = bytearray(16)
    i_old_block3 = bytearray(16)
    i_old_blocks = [i_old_block1,i_old_block2,i_old_block3]

    # for i in range(3):
    #     prev_c = c_old_blocks[i]
    #     p = p_old_blocks[i+1]
    #     block = i_old_blocks[i]
    #     for j in range(16):
    #         block[j] = prev_c[j] ^ p[j]

    i_block1 = bytearray(16)
    i_block2 = bytearray(16)
    i_block3 = bytearray(16)
    i_blocks = [i_block1,i_block2,i_block3]

    p_block = p_old_blocks[2]
    c_block = c_old_blocks[2]
    for byte_no in range(16):
        i_block3[byte_no] = p_block[byte_no] ^ c_block[byte_no]

    nc = b''
    for i in range(2,-1,-1):
        i_block = i_blocks[i]
        p_block = p_new_blocks[i]
        new_cipher_block = b''
        for j in range(16):
            i_bits = format(i_block[j], '008b')
            p_bits = format(p_block[j], '008b')
            for k in range(8):
                if i_bits[k] != p_bits[k]:
                    new_cipher_block = new_cipher_block + b'1' #change ciphertext
                else:
                    new_cipher_block = new_cipher_block + b'0' #dont change
        
        c_new_blocks[i] = bytearray(bytes(int(new_cipher_block[i : i + 8], 2) for i in range(0, len(new_cipher_block), 8)))

        if(i > 0):
            message = ""
            b_block = b'\x02\x02'
            b_block = bytearray(b_block)
            i_block = bytearray(16)
            p_block = p_new_blocks[i-1]
            c_block = c_old_blocks[i-1]
            message = c_old_blocks[i-1]+c_new_blocks[i]+b_block
            message_b64 = base64.b64encode(message)
            message_b64 = message_b64.decode('utf-8') #convert to string
            message_b64 = message_b64.replace('=', '%3D') #make url safe
            message_b64 = message_b64.replace('+', '%2B')
            message_b64 = message_b64.replace('/', '%2F')
            url = 'http://gruenau5.informatik.hu-berlin.de:8888/store_secret/'+message_b64
            command = subprocess.Popen(["curl","--silent",url], stdout = subprocess.PIPE)
            answer = command.communicate()
            print("vvvv")
            print(answer)
            print("^^^^")
            block = i_blocks[i-1]
            for byte_no in range(16):
                block[byte_no] = p_block[byte_no] ^ c_block[byte_no]
            

        #print(new_cipher_block) #write dat shit into c_block3,2,1
        nc = new_cipher_block + nc

    #print(nc)
    nc_bytes = bytes(int(nc[i : i + 8], 2) for i in range(0, len(nc), 8))
    nc_bytes = nc_bytes + c_old_block4
    nc_hex = hex(int(nc, 2))
    nc_bytes_b64 = base64.b64encode(nc_bytes)
    #print(nc_bytes_b64)
    nc_bytes_b64 = nc_bytes_b64.decode('utf-8') #convert to string
    nc_bytes_b64 = nc_bytes_b64.replace('=', '%3D') #make url safe
    nc_bytes_b64 = nc_bytes_b64.replace('+', '%2B')
    nc_bytes_b64 = nc_bytes_b64.replace('/', '%2F')

    





        


    





    


 





