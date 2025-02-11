
def normalize_data(value):
    """Normalize data by removing spaces and converting to lowercase."""
    return value.replace(" ", "").lower() if isinstance(value, str) else value
