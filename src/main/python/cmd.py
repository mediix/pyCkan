import __builtin__
import argparse
from database import set_connection

def main():
    """Entry point to establish mysql conneciton"""
    parser = argparse.ArgumentParser(prog='pydev')
    parser.add_argument('-u', nargs='?', help='username', type=str, default='')
    parser.add_argument('-p', nargs='?', help='password', type=str, default='')
    parser.add_argument('-s', nargs='?', help='host', type=str, default='')
    parser.add_argument('-d', nargs='?', help='database', type=str, default='')

    args = parser.parse_args()

    if '' in [args.u, args.p, args.s, args.d]:
        raise ValueError('Got empty value, Try Again...')
        return

    try:
        con = set_connection(args.u, args.p, args.s, args.d)
        __builtin__.con = con
    except Exception as err:
        raise ValueError(err)
    else:
        print "Connection successfully established."

def ckan_fetch():
    """
    """



# def ckan_update():
#     """
#     """

# def ckan_verify():
#     """
#     """
