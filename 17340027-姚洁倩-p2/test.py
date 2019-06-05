def error():
    raise ValueError

if __name__ == "__main__":
    try:
        error()
    except:
        raise ValueError