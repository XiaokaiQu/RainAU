def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

def clean_NA(v):
    if v == 'NA':
        return False
    else:
        return True