import base64

class Base64ToolBox:
    
    @staticmethod
    def encode(original_string):
        encoded_bytes = base64.b64encode(original_string.encode('utf-8'))
        return encoded_bytes.decode('utf-8')
    
    @staticmethod            
    def decode(encoded_string):
        decoded_bytes = base64.b64decode(encoded_string)
        return decoded_bytes.decode('utf-8')