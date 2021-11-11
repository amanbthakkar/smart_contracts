# quit the ui when writing tests
from brownie import network, accounts, exceptions
from scripts.deploy import deploy_fund_me
from scripts.fund_and_withdraw import fund
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    # now we fund
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.funds(account.address) == entrance_fee
    # and now withdraw
    tx2 = fund_me.withdrawAllFunds({"from": account})
    tx2.wait(1)
    assert fund_me.funds(account.address) == 0


# see default can be changed in config file
# but what if u dont want ur tests to be done on rinkeby?
# install pytest


def test_only_owner_can_withdraw():
    if (
        network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS
    ):  # gonna be skipping for mainnet-fork-dev as it is not in local bc networks
        pytest.skip("Only for local testing")
    print(network.show_active())
    fund_me = deploy_fund_me()
    # now we want to withdraw with some other account
    bad_actor = accounts.add()
    # fund_me.withdrawAllFunds({"from": bad_actor}) #VM errors we will get, but how to test?
    # import exceptions
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdrawAllFunds({"from": bad_actor})


# brownie test -k test_only_owner_can_withdraw --network rinkeby
# it will skip this test
# brownie test --network development
# it will happen
