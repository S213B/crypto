import hashlib
import random

class Base:
    p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
    g = 2
    k = 3

    def get_rand(self, bit):
        return random.getrandbits(bit) % self.p

    def my_pow(self, x):
        return pow(self.g, x, self.p)

    def str2int(self, s):
        h = hashlib.sha256(s).hexdigest()
        x = int(h, 16)
        return x

class Server(Base):
    salt = None
    client_list = {}

    def __init__(self):
        self.salt = self.get_rand(200)
        return

    def add_client(self, email, password):
        x = self.str2int(str(self.salt) + password)
        v = self.my_pow(x)
        b = self.get_rand(200)
        self.client_list[email] = {'v':v, 'b':b}
        return self

    def get_client(self, email):
        if email in self.client_list:
            return self.client_list[email]
        else:
            #print "Not valid user or password"
            return None

    def get_salt(self):
        return self.salt

    def get_pub_key(self, email):
        salt = self.get_salt()
        client_info = self.get_client(email)
        if client_info is None:
            return None, None, None
        b = client_info['b']
        u = None
        if 'u' in client_info:
            u = client_info['u']
        else:
            u = self.get_rand(128)
            client_info['u'] = u
        B = self.my_pow(b)
        return salt, B, u

    def rcv_pub_key(self, email, A):
        client_info = self.get_client(email)
        if client_info is None:
            return self
        v = client_info['v']
        b = client_info['b']
        u = None
        if 'u' in client_info:
            u = client_info['u']
        else:
            u = self.get_rand(128)
            client_info['u'] = u

        S = (pow(A, b, self.p) * pow(v, u * b, self.p)) % self.p
        #S = pow(A * pow(v, u), b, self.p)
        #print S
        K = hashlib.sha256(str(S)).hexdigest()
        #print K
        client_info['valid'] = hashlib.sha256(K + str(self.get_salt())).hexdigest()
        return self

    def valid(self, email, v):
        client_info = self.get_client(email)
        if client_info is None:
            print "Not valid user or password"
            return False
        r = client_info['valid']
        #print r
        #print v
        if r != v:
            print "Not valid user or password"
            return False
        return True

class Client(Base):
    email = None
    password = None
    pri_key = None
    pub_key = None

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.pri_key = self.get_rand(200)
        self.pub_key = self.my_pow(self.pri_key)
        return

    def get_email(self):
        return self.email

    def get_pub_key(self):
        email = self.get_email()
        return email, self.pub_key

    def get_passwd(self):
        return self.password

    def rcv_pub_key(self, salt, B, u):
        if (salt is None) or (B is None) or (u is None):
            return None
        x = self.str2int(str(salt) + self.get_passwd())

        S = pow(B, (self.pri_key + u * x), self.p)
        #print S
        K = hashlib.sha256(str(S)).hexdigest()
        #print K
        return hashlib.sha256(K + str(salt)).hexdigest()

class Attacker(Server):
    salt = None
    b = None
    B = None
    u = None
    passwd = ['1', '2', '3', '123', '111', '222', '333', 'password', 'asdf', 'qwer', 'aaa']

    def __init__(self):
        self.salt = self.get_rand(200)
        self.b    = self.get_rand(200)
        self.B    = self.my_pow(self.b)
        self.u    = self.get_rand(128)
        return

    def get_pub_key(self, email):
        return self.salt, self.B, self.u

    def rcv_pub_key(self, email, A):
        self.client_list[email] = A
        return self

    def valid(self, email, target):
        for p in self.passwd:
            A = self.get_client(email)
            if A is None:
                print "Do not have public key of", email
                return False
            salt = self.salt
            b = self.b
            u = self.u
            N = self.p

            # compute v
            x = self.str2int(str(salt) + p)
            v = self.my_pow(x)

            S = (pow(A, b, N) * pow(v, u * b, N)) % N
            K = hashlib.sha256(str(S)).hexdigest()
            guess = hashlib.sha256(K + str(salt)).hexdigest()

            if target == guess:
                print "Password is", p
                return True

        return False


        v = client_info['v']

        S = (pow(A, b, self.p) * pow(v, u * b, self.p)) % self.p
        #S = pow(A * pow(v, u), b, self.p)
        #print S
        K = hashlib.sha256(str(S)).hexdigest()
        #print K
        client_info['valid'] = hashlib.sha256(K + str(self.get_salt())).hexdigest()



        client_info = self.get_client(email)
        if client_info is None:
            print "Not valid user or password"
            return False
        r = client_info['valid']
        #print r
        #print v
        if r != v:
            print "Not valid user or password"
            return False
        return True

def main():
    s = Server()

    print "Register"
    user = raw_input("user name:")
    passwd = raw_input("password:")
    s.add_client(user, passwd)

    print "Login"
    user = raw_input("user name:")
    passwd = raw_input("password:")
    c = Client(user, passwd)

    I, A = c.get_pub_key()
    s.rcv_pub_key(I, A)

    salt, B, u = s.get_pub_key(I)
    v = c.rcv_pub_key(salt, B, u)

    if s.valid(I, v):
        print "Passed"
    else:
        print "Failed"

    #MITM
    print "MITH:"
    a = Attacker()

    I, A = c.get_pub_key()
    a.rcv_pub_key(I, A)

    salt, B, u = a.get_pub_key(I)
    v = c.rcv_pub_key(salt, B, u)

    if a.valid(I, v):
        print "Cracked"
    else:
        print "Crack failed"

if __name__ == "__main__":
    main()
