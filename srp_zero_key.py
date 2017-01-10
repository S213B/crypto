import hashlib
import random

class Base:
    p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
    g = 2
    k = 3

    def get_rand(self):
        return random.getrandbits(200) % self.p

    def my_pow(self, x):
        return pow(self.g, x, self.p)

    def str2int(self, s):
        h = hashlib.sha256(s).hexdigest()
        x = int(h, 16)
        return x

    def get_prime(self):
        return self.p

class Server(Base):
    salt = None
    client_list = {}

    def __init__(self):
        self.salt = self.get_rand()
        return

    def add_client(self, email, password):
        x = self.str2int(str(self.salt) + password)
        v = self.my_pow(x)
        b = self.get_rand()
        self.client_list[email] = {'v':v, 'b':b}
        return self

    def get_client(self, email):
        return self.client_list[email]

    def get_salt(self):
        return self.salt

    def get_pub_key(self, email):
        salt = self.get_salt()
        client_info = self.get_client(email)
        v = client_info['v']
        b = client_info['b']
        B = self.k*v + self.my_pow(b)
        client_info['B'] = B
        return salt, B

    def rcv_pub_key(self, email, A):
        client_info = self.get_client(email)
        v = client_info['v']
        b = client_info['b']
        if 'B' in client_info:
            B = client_info['B']
        else:
            B = self.k*v + self.my_pow(b)
        u = self.str2int(str(A) + str(B))

        S = (pow(A, b, self.p) * pow(v, u * b, self.p)) % self.p
        #S = pow(A * pow(v, u), b, self.p)
        print 'Server S:', S
        K = hashlib.sha256(str(S)).hexdigest()
        #print K
        client_info['valid'] = hashlib.sha256(K + str(self.get_salt())).hexdigest()
        return self

    def valid(self, email, v):
        client_info = self.get_client(email)
        r = client_info['valid']
        #print r
        #print v
        return r == v

class Client(Base):
    email = None
    password = None
    pri_key = None
    pub_key = None

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.pri_key = self.get_rand()
        self.pub_key = self.my_pow(self.pri_key)
        return

    def get_email(self):
        return self.email

    def get_pub_key(self):
        email = self.get_email()
        return email, self.pub_key

    def get_passwd(self):
        return self.password

    def rcv_pub_key(self, salt, B):
        u = self.str2int(str(self.pub_key) + str(B))
        x = self.str2int(str(salt) + self.get_passwd())

        S = pow(B - self.k * pow(self.g, x, self.p), (self.pri_key + u * x), self.p)
        #S = pow(B - self.k * pow(self.g, x), (self.pri_key + u * x), self.p)
        #print 'Client S:', S
        K = hashlib.sha256(str(S)).hexdigest()
        #print K
        return hashlib.sha256(K + str(salt)).hexdigest()

def main():
    s = Server()
    c = Client("abc@def.com", "123456")
    s.add_client(c.get_email(), c.get_passwd())

    #I, A = c.get_pub_key()
    I = c.get_email()
    A = 0
    #A = c.get_prime()
    #A = c.get_prime() * c.get_prime()
    #A = pow(c.get_prime(), 213)
    s.rcv_pub_key(I, A)

    salt, B = s.get_pub_key(I)
    #v = c.rcv_pub_key(salt, B)
    v = hashlib.sha256(hashlib.sha256(str('0')).hexdigest() + str(salt)).hexdigest()

    if s.valid(I, v):
        print "Passed"
    else:
        print "Failed"

if __name__ == "__main__":
    main()
