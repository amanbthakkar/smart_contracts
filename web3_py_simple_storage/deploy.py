from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

install_solc("0.6.0")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# once we read, we have to compile the file
# py-solc-x can be used for that

# Compile our code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# from the above file you can get your abi related info which is talked about so much

# Now deploy it - need bytecode and abi to deploy to a chain

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# where are we gonna deploy it to? On remix we were using a simulated - JavaScript VM
# this is where Ganache comes in - fake bc that we can deploy contracts to
# to connect to ganache we need web3, and HTTP provider
# ganache has RPC server which has a url
# in remix we use Metamask directly to connect to blockchain

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# need ID of blockchain/network
chain_id = 1337

# need address to deploy from
my_address = "0x59ED98c623066B3974F0A0BE5e4003Bada1Cf82D"  # any random address
private_key = "0x"  # take its private key

# first create the contract using abi and bytecode
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# how to deploy it? we need to build a txn to deploy this contract. just like on remix.
# now nonce in this case is just transaction number for a particular address. will be 0 at start.
nonce = w3.eth.getTransactionCount(my_address)  # print this and its 0 at the beginning
print(nonce)
# build, sign and send a transaction
print("Deplying contract...")
# first build a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)
# print(transaction)

# then sign the transaction
private_key = os.getenv("PRIVATE_KEY")

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# then send it to the chain via a transaction so it can actually get deployed
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# you can wait for some block confirmations too.
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!!")

# now contract is sent to blockchain (deployed)- OK. But how do we work with this contract? How to interact?
# so far what we've done is equivalent to pressing Deploy button on remix
# I guess it is like writing a class and sending the code to the blockchain

# To interact, we always need 2 things: contract address and contract abi
# need to make a new contract object to work with a contract
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# print(simple_storage.functions.retrieve())
# output of above: <Function retrieve() bound to ()>

# While making transactions with a blockchain, there are 2 different ways to interact with them
# 1. Call() -> simulate making the call and getting a return value - they don't actually make a state change to the blockchain
# its like the blue buttons on remix - nothing actuall changes on the blockchain there
# you can actually "call" the orange functions also (which are non-view ones) but remix defaults them to be "transacts"
# 2. Transact() -> we actually make a state change. used to build & send a transaction
# you can always transact on a function even if it is a view - and it will attempt to make a state change

# so we do call() on retrieve function - as there is no state change
print(simple_storage.functions.retrieve().call())

print(simple_storage.functions.store(5).call())
# none of these are actually added to the blockchain as transactions as they are mereley simulations. call retrieve() and it'll still be 0

# so now lets build a txn to store some new value in the contract. need to follow same steps as above.

# build, sign and send a transaction
# first build a transaction
# transaction = SimpleStorage.constructor().buildTransaction(
#    {"chainId": chain_id, "from": my_address, "nonce": nonce}
# )
print("Updating contract.....")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)
# this stays same, just a new name & function instead of constructor - make sure nonce is updated though

# signing is same too
private_key = os.getenv("PRIVATE_KEY")

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

# then send it to the chain via a transaction so it can actually get deployed
transaction_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
# you can wait for some block confirmations too.
tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
print("Updated!!")

# THEREFORE to build a transaction, use the contract's constructor
# once that is done, to interact with the transaction use contract's function().name(add_parameters).buildTransaction({})
# for simply "calling" we were using simple_storage -> which was the object of the contract
# for actual "transact", we were building a txn using simple_storage -> which was object of the contract
# thus the function()._name_() belongs to the object of the contract created

print(simple_storage.functions.retrieve().call())
# this will now give updated value which has been written to blockchain
# hmm now to interact with ganache using CLI (which Brownie uses) we actually need Node js.
