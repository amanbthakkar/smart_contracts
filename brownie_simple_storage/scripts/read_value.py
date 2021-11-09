# read values directly from blockchain
# we used address and abi in web3

from brownie import SimpleStorage, accounts, config


def read_contract():
    # so how to interact?
    # SimpleStorage is just an array! It has a list of contracts deployed
    # print(SimpleStorage[0]) => 0 is 1st, -1 is the latest contract
    simple_storage = SimpleStorage[-1]  # easy!
    # we dont need abi and address explicitly - address is saved in deployments/ and abi is in the json file in contracts/ after compiling
    print(simple_storage.retrieve())


def main():
    read_contract()
