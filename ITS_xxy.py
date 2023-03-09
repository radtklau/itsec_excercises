#28 b4 3e 63 17 c3 a1 5d f5 09 68 26 50 4f dc a9 f2 1c a9 c3 e5 5e 89 1c ae 72 aa 1e 75 a9 07 46 2f dc 24 d0 be 21 b4 71 a1 2f 29 c8 13 a5 7f 41 cc 94 6b e4 1b 66 ad 10 4b 16 0f 23 06 46 dd db
#4 blocks
#1: 28 b4 3e 63 17 c3 a1 5d f5 09 68 26 50 4f dc a9
#2: f2 1c a9 c3 e5 5e 89 1c ae 72 aa 1e 75 a9 07 46
#3: 2f dc 24 d0 be 21 b4 71 a1 2f 29 c8 13 a5 7f 41
#4: cc 94 6b e4 1b 66 ad 10 4b 16 0f 23 06 46 dd db

#hallo = 68 61 6C 6C 6F 0B 0B 0B 0B 0B 0B 0B 0B 0B 0B 0B

import base64
from paramiko import SSHClient
import paramiko as paramiko
import os

cipher = "KLQ+YxfDoV31CWgmUE/cqfIcqcPlXokcrnKqHnWpB0Yv3CTQviG0caEvKcgTpX9BzJRr5BtmrRBLFg8jBkbd2w=="

cipher_hex = base64.b64decode(cipher)

testbyte = 0

size = 16
p2 = bytearray(size)
i2 = bytearray(size)

def connect_to_server(adr,user,pw):
    server = SSHClient()
    server.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    server.connect(adr,username=user,password=pw)
    return server

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

block1 = bytearray(cipher_hex[:16])
block2 = bytearray(cipher_hex[16:32])
block3 = bytearray(cipher_hex[32:48])
block4 = bytearray(cipher_hex[48:])
blocks = [block1,block2,block3,block4]

server = connect_to_server('gruenau5.informatik.hu-berlin.de','radtklau','tangen+ezaHnreg4l')
message = ""

def decrypt_block(block_no):
    for byte_no in range(16):
        c1fake = bytearray(os.urandom(16))

        for j in range(byte_no): #calc c1fake for valid padding
            c1fake[-(j+1)] = i2[-(j+1)] ^ byte_no+1 #c'1[16] ^ i2 = 02


        for test_hex in range(256): #find byte for correct padding
            c2 = blocks[-(block_no+1)]
            testbyte = test_hex #hex(i)?

            c1fake[-(byte_no+1)] = testbyte
            #print(c1fake)
            c1fake_c2 = bytes(c1fake) + bytes(c2) #merge

            #print(c1fake_c2)
            #encode
            c1fake_c2_b64 = base64.b64encode(c1fake_c2)
            #print(c1fake_c2_b64)
            c1fake_c2_b64_str = c1fake_c2_b64.decode('utf-8')
            c1fake_c2_b64_str_urlsafe = c1fake_c2_b64_str.replace('=', '%3D')
            c1fake_c2_b64_str_urlsafe = c1fake_c2_b64_str_urlsafe.replace('+', '%2B')
            c1fake_c2_b64_str_urlsafe = c1fake_c2_b64_str_urlsafe.replace('/', '%2F')
            
            #print(c1fake_c2_b64_str_urlsafe)
            #send to server
            command = 'curl  http://gruenau5.informatik.hu-berlin.de:8888/store_secret/'+c1fake_c2_b64_str_urlsafe
            stdin, stdout, stderr = server.exec_command(command) 
            answer = stdout.readlines() #get answer

            #print(answer[0])
            if answer[0] == 'Secret succesfully received':
                print(testbyte)
                print(hex(test_hex))
                print(test_hex)
                #server.close()
                break

        bl = blocks[-(block_no+2)]
        i2[-(byte_no+1)] = testbyte ^ byte_no+1
        p2[-(byte_no+1)] = bl[-(byte_no+1)] ^ i2[-(byte_no+1)]
        print(bytes(p2))

    return(bytes(p2).decode("utf-8"))

if __name__ == "__main__":
    

    


 





