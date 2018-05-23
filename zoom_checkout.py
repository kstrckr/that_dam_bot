import os
import subprocess

class ZmCheckoutSession:
    '''
    returns 234 if authentication/relogin required, else returns 0 for successful checkout/download
    '''

    base_args = ['zm', 'checkout', '--nowc', '-d']

    @classmethod
    def checkout_a_dir(self, local_dir, dir_to_checkout):

        args = list(self.base_args)

        if os.path.exists(local_dir):
            args.append(local_dir)
        
        args.append(dir_to_checkout)

        p = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        try:
            print(u'Downloading {}'.format(dir_to_checkout))
            checkout_process = p.communicate()

            if checkout_process[1] == 234:
                return 234

            else:
                print('Succesfully downloaded {}'.format(dir_to_checkout))
                return 0
        
        except subprocess.CalledProcessError:

            return -1