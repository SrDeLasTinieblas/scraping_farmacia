import base64

import hashlib

#unique_text = lambda text: hashlib.sha256(text.encode('utf-8')).hexdigest()
unique_text = lambda *args: hashlib.sha256(''.join(map(str, args)).encode('utf-8')).hexdigest()

separator = "|"

def tuple_to_hyphenated_string(triple):
        return separator.join(map(str, triple))

def hyphenated_string_to_tuple(string):
        return tuple(string.split(separator))
    

def encode_base64(input_string):
    try:
        encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
        encoded_string = encoded_bytes.decode('utf-8')
        return encoded_string
    except Exception as e:
        print(f"Error encoding base64: {e}")
        return None
    
def decode_base64(encoded_string):
    try:
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
    except Exception as e:
        print(f"Error decoding base64: {e}")
        return None
