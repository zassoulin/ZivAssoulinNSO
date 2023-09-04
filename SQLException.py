class SQLException(Exception):
    """Exception raised for errors in the database."""

    def __init__(self, message):  # creating exceptions to prevent debug info from being sent to the client
        super().__init__(message)
