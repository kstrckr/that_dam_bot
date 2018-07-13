import subprocess

class Authenticator:



    def __init__(self):
        
        self.enter_credentials()

    def login(self):

        auth_args = ['zm', '-s', 'EvolProd', '--username', self.user, '--password', self.pw, 'getcredentials']

        p = subprocess.Popen(auth_args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        interface = p.communicate()
        
        if p.returncode == 0:
            print("Login Successful")
            # logging.info("Sucesfully Logged Back in at {}".format(return_strf_now()))
            return True
        else:
            print(interface[1])
            return False
            # logging.debug('Login ERROR at {}'.format(return_strf_now()))

    def enter_credentials(self):

        self.user = raw_input("\nEnter Username: ")
        self.pw = raw_input("Enter Password: ")

if __name__ == "__main__":

    login = Authenticator()

    login.login()