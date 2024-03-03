from config import DEBUG

def debugp(*arg, **krgs):
    if DEBUG:
        print(*arg, **krgs)