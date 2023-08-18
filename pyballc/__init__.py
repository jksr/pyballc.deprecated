from .pyballc import *
import fire

def main():
    fire.core.Display = lambda lines, out: print(*lines, file=out)
    fire.Fire()
