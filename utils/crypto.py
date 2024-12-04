from utils import *

if __name__ == '__main__':
    # Encrypt all input files
    en_decrypt_file_types("../inputs/", "key.key", encrypt=True, override_file=False, regex_file_match=r".+(\.txt)$", remove_extension="", add_extension=".enc")

    # Decrypt all input files
    # en_decrypt_file_types("../inputs/", "key.key", encrypt=False, override_file=False, regex_file_match=r".+(\.enc)$", remove_extension=".enc", add_extension="")

