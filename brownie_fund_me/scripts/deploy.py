from brownie import FundMe, MockV3Aggregator, network, config
from web3 import Web3
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)

# as ganache-local is not development, we add LOCAL_BLOCKCHAIN_ENVIRONMENTS to helpful_scripts
# LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


DECIMALS = 8
STARTING_PRICE = 200000000000
# what are these? see below


def deploy_fund_me():
    account = get_account()

    if (
        network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS
    ):  # no mainnet over here because we need to deploy mock for local ones only
        # price_feed_address = config["networks"]["rinkeby"]["eth_usd_price_feed"] is equivalent to
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]  # i.e. if not on development network, take value from config
    else:
        # deploy a mock
        # create a test/ inside contracts/
        # this is usually where mocks go -> take from chainlink-mix from github for now
        # brownie compile again
        # lets deploy the mocks
        print(f"Active network is {network.show_active()}")
        print("Deploying mocks...")
        # in below statement we are deploying MockAggregator on every run... but since it might have already been deployed once
        # we can simply reuse it from MockV3Aggregator[-1]:

        # if len(MockV3Aggregator) <= 0:
        #    mock_aggregator = MockV3Aggregator.deploy(
        #        DECIMALS,
        #        Web3.toWei(STARTING_PRICE, "ether"),
        #        {"from": account},  # note the change later in helpful scripts
        #    )  # towei just adds 18 0s lol, see constructor parameters of the contract to understand why 18 and 2000 is passed

        # and this entire code of deploying a mock can be shifted to helpful_scripts

        deploy_mocks()  # from helpful scripts
        print("Mocks deployed...")
        price_feed_address = MockV3Aggregator[
            -1
        ].address  # if its already deployed then just take the latest one

    # now that we have the price_feed_address for either case we can proceed to call constructor of FundMe and deploy.

    fund_me = FundMe.deploy(
        price_feed_address, {"from": account}
    )  # this is how you pass variables to constructors... similar to calling function with a parameter
    # but then again hardcoding 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e as a constructor parameter will not work
    # as it is ultimately a rinkeby address and we want a local address..

    print(f"Contract deployed to {fund_me.address}")
    # brownie run scripts/deploy.py --network rinkeby
    return fund_me


# issues with working with ganache: our fund_me contract has hardcoded chainlink addresses
# these addresses are very specific to rinkeby
# this makes it hard to work with not only local blockchain but also any other kind like kovan or mainnet or whatever
# 1. Forking 2. Mocking
# Mocking is common - fake version of version and interact as if it is real - MockAggregator explained in a bunch of places
# Forking - mainnet-fork
# this involves setting up a copy - Patrick uses alchemy instead of infura for this
# this part comes after everything else in the entire folder
# mainnet-fork -> add to networks in config
# but now when u run, u get error: insufficient funds (running on mainnet-fork)
# because we do accounts.add(config) when it is in local blockchain env and otherwise we do rinkeby account add
# we have one LOCAL_ENV variable. but that same variable is also used to deploy a mock for local development. mainnet-fork however already has a contract.
# so we create a new env variable
# again if u run, there is error. (list index) because brownie's inbuilt forking mechanism doesnt come with its own accounts i.e. accounts[0] is not there for forks
# so we create a custom mainnet-fork for development using "add" key in brownie networks
# brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-mainnet.alchemyapi.io/v2/cl0nS1khC7VRXx8FpsNbFfZQHbXurbj8 accounts=10 mnemonic=brownie port=7545
# development env instead of persistent, command to run it is called ganache-cli
# a new network mainnet-fork-dev should be added. patrick actually deletes og one and replaces it with this (names it just mainnet-fork)

# now - if you open ganache and keep, brownie is smart enough to detect that it is open and then uses that CLI instead
# remember however that local deployments are not saved in the build/
# only the rinkeby ones is saved (under folder 4/, as it is saved under chain_id)
# so how to get even the local ones saved? that we want brownie to remember?
# brownie networks list => give list
# u can add any evm blockchain here --> brownie networks add Ethereum (or local) ganache-local host=<RPC HTTP ADDRESS> chain_id=1337
#
# now u can do brownie run scripts/deploy.py --network ganache-local. keep ganache UI up!
# but note - ganache-local is not a development env so it tries to pull the values from config file
# hence we set up LOCAL_BLOCKCHAIN_ENVIRONMENTS in helpful_scripts and use it where needed
# now if we deploy local it gets stored in deplyments/ under 1337/

# in case u close the UI and want to reset, you can delete the 1337 chain and then its entries from map.json OR delete whole folder
# now proceed to interacting with the file - can fund the contract and all
def main():
    deploy_fund_me()
