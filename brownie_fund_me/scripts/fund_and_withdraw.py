from brownie import FundMe, network, config
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    # now we will use functions on top of fund_me which is the object
    # now find out how much is required as entrance fee
    entrance_fee = fund_me.getEntranceFee()   # safe side
    print(entrance_fee)
    price = fund_me.getPrice()
    print(f"Price is {price}")
    print("Now funding")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdrawAllFunds({"from": account})


def main():
    fund()
    withdraw()
