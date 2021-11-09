from brownie import accounts, config, SimpleStorage, network

# import os - not needed if config file


# native accounts package - can add accounts in many different ways

# if working with local chain - ganache has 10 accounts
def deploy_simple_storage():
    # account = accounts[0]  # great for development network i.e. the local ganache one
    account = get_account()
    # load the account created through terminal as explained below (after whole function)
    # account = accounts.load("fcc-account")
    # often you want to use a mix

    # 3rd way, env variable => now this is handled well by brownie
    # make a file called "brownie-config.yaml" after making the .env file.
    # brownie knows to look here
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # print(account)

    # but actually you can add more info to the yaml file
    # what wallets to use, and when?
    # account = accounts.add(config["wallets"]["from_key"]) #same as os.getenv, but now can pull from one place

    # we can actually import contract directly: from brownie import SimpleStorage
    simple_storage = SimpleStorage.deploy({"from": account})
    # any time u deploy to chain or make a txn and tell which address is actually deploying. much faster than bytecode/abi/nonce etc
    # brownie knows if its a transact() or a call()
    # simple_storage is now a contract object

    # now we store 15 and retrieve
    stored_value = simple_storage.retrieve()  # this is a call so dont need a "from"
    print(stored_value)
    # to transact() and actually store a value
    # REMEMBER ONCE THE CONTRACT IS DEPLOYED YOU WORK WITH THE OBJECT, i.e. simple_storage and not SimpleStorage anymore
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)  # wait for number of blocks
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)
    # now check tests so that you dont have to again and again test the output.


# what to do with tesnet? use CLI and add natively to brownie
# brownie accounts new fcc-account => type this and enter your private key from metamask (remember to add 0x at beginning)
# this is the most secure method
# view it by - brownie accounts list
# remove by - brownie accounts delete <nameOfAccount>

# now deploy to a testnet

# run "brownie networks list"
# development networks - default, temporary, like ganache and all
# ethereum - persistent
# in web3 we used http provider/RPC
# how to get url? brownie knows infura's => go to .env file
# can run
# brownie run scripts/deploy.py --networks rinkeby
# but here we need our private key, not local ganache
# use get_account() to switch easily


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        # pull from config file yaml as defined above
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
    # brownie run scripts/deploy.py --network rinkeby


# note build/contracts change
# deployments are saved, can go back and see what happened
# separated by chainid
# development section deployments are not saved.
# now we can interact with contracts already deployed to a chain! ------> new read_value.py


#brownie console
#>> makes a console with everything imported
# brand new local test environment 
# use as python interpreter basically 
# can do account = accounts[0] ==> everything we import from brownie is imported readymande
# can easily deploy contracts and all