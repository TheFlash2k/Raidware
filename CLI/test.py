import enum
from socket import socket
import sys
sys.dont_write_bytecode = True

# sys.path.append("listeners/non_staged")
# # sys.path.append("non_staged")

# data = __import__('tcp')
# print(data.Listener())


# def fetch_config(protocol : str) -> dict:
    
#     import configparser
#     import re

#     config = configparser.ConfigParser()

#     file = f"listeners/default.conf"

#     config.read(file)
#     try:
#         data = config[protocol.upper()]


#         ret = {}
#         for item in data:
#             curr = data[item].replace('"','')
#             if data[item][0] == '[' and data[item][-1] == ']':
#                 curr = data[item].replace('[','').replace(']','').replace('"','').strip().split(',')

#             ret[item] = curr

#     except KeyError:
#         return None

#     return ret


# print(fetch_config("tcp"))


def run(msg, **kwargs):
    print(kwargs)

s = socket()

run("hellpo", socket=s)