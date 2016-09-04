openssl enc -in one_seven.txt -d -base64 -K $(echo -n "YELLOW SUBMARINE" | xxd -ps) -aes-128-ecb -out tmp.txt
