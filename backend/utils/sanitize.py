import  html
import re 

def sanitize_input(input_string):
    # Strip HTML tags and escape HTML characters in one line
    safe_string = html.escape(re.sub(r'<[^>]*>', '', str(input_string)))
    return safe_string