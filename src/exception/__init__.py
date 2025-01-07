import sys
import logging

def error_message_detail(error: Exception, error_detail: sys) -> str:

    # Extract traceback details (exp info)
    _, _, exc_tb = error_detail.exc_info()
    
    # Get the file name where the exception occured
    file_name = exc_tb.tb_frame.f_code.co_filename
    
    # Create a formatted error message string with file name, line number, and the actual error
    line_number = exc_tb.tb_lineno
    error_message = f"Error occured in pyhton script: [{file_name}] at line number [{line_number}]: {str(error)}"
    
    # Log the error for better tracking
    logging.error(error_message)
    
    return error_message

class MyException(Exception):
    """
    Custom exception class for handling errors in the US visa application.
    """
    
    def __init__(self, error_message: str, error_detail: sys):
        """
        Initializes the USvisaException with a detailed error message.

        :param error_message: A string describing the error.
        :param error_detail: The sys module to access traceback details.
        """
        
        # Call the base class constructor with the error msg
        super().__init__(error_message)
        
        # Formatting the detailed error msg using the error_message_detail func
        self.error_message = error_message_detail(error_message, error_detail)
        
    def __str__(self) -> str:
        """
        Returns the string representation of the error message.
        """
        return self.error_message