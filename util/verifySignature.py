import gnupg

class KeyImportError(Exception):
    pass

class verifySignature:

    def __init__(self):
        self.__gpg = gnupg.GPG()

        self._key_data = """
-----BEGIN PGP PUBLIC KEY BLOCK-----

mDMEZ2x3lBYJKwYBBAHaRw8BAQdAs0RYLmWE3W4IshiMeioSk5/WUxvDr10XyHqe
ym6xrTm0Hkphc29uIEpvaG5zb24gPGszanNqQGFycmwubmV0PoiWBBMWCAA+AhsD
BQkSzAMAAh4BAheAFiEEghrFRG0biB8oXS/2plFIwV6lUw4FAmdseG4FCwkIBwMF
FQoJCAsFFgIDAQAACgkQplFIwV6lUw7ufAD/SHvb2DPQP+LXtUP5QtZUsb008vev
PY3nPIiiHJLySYgA/Agin0ZFdi2zSgKA0NlBCCOf6LAtyjuIU9BtuiowhmoFuDME
Z2x4hBYJKwYBBAHaRw8BAQdA8rTNYtQRtdHi0PLFBebZNoVv3QeFRAJ5QdpK7f75
DbaI9QQYFggAJhYhBIIaxURtG4gfKF0v9qZRSMFepVMOBQJnbHiEAhsCBQkDwmcA
AIEJEKZRSMFepVMOdiAEGRYIAB0WIQR+IRDUkGkAJUU5yYJZwtXH9CXoAgUCZ2x4
hAAKCRBZwtXH9CXoAmTtAPwLUKq/UDb5GMvfjnzvNQYRaYh5dHWJzHXEOHsd86mT
8AD/ZqMOHUjC0sb05HRVko44okoFCfXWmTGbb8ARby2+HQvluAEAoN4IuEXRfDlz
r4Tqa8k6JJZcPpAOhQL2DCzRbUbogxsBAOKOVziWFKR5kM2g6B1hkDq5qvKLUErd
J4+yQOCXMlkAuDgEZ2x4sxIKKwYBBAGXVQEFAQEHQDY1QjTkHAuFqx+RN9HnQwfR
pz7bW9+lxaiInFGUoUx4AwEIB4h+BBgWCAAmFiEEghrFRG0biB8oXS/2plFIwV6l
Uw4FAmdseLMCGwwFCQPCZwAACgkQplFIwV6lUw4D6QEAsiP7V6mtkMW01albjEAf
T1UrxEjctC/ZAbY4JWAw/asBAM7cM+3rj/07bStJkxyuvq4wXu9IAs+eEIP3USgb
RtoEuDMEZ2x4wBYJKwYBBAHaRw8BAQdAT8HPg/SWHQIkjOzRdcB7zQvbvl0imBQN
GDb9TnKr8fyIfgQYFggAJhYhBIIaxURtG4gfKF0v9qZRSMFepVMOBQJnbHjAAhsg
BQkDwmcAAAoJEKZRSMFepVMOGakBAMVcxkLcgc1JOVMdGF/g6FUcq4s49EAh74wg
PVDT7y0SAQCm8pihahsOWtdKbanP3b+XA08Y87pZZ6bsQol2fIOSAQ==
=uFDz
-----END PGP PUBLIC KEY BLOCK-----
    """

        # Import the key
        self.__import_result = self.__gpg.import_keys(self._key_data)

        # Check the result
        if not self.__import_result.count:
            raise KeyImportError("Could not read key")

    def verifyFile(self,file_name, signature_file):

        # Read the signed file
        with open(file_name, 'rb') as f:
            signed_data = f.read()

        # Read the signature file
        with open(signature_file, 'rb') as f:
            signature_data = f.read()

        # Verify the signature
        verify_result = self.__gpg.verify_data(signature_file, signed_data)

        # Check the result
        return verify_result.valid
