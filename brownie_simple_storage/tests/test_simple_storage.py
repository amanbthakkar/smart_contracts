# this file has to start with test
from brownie import SimpleStorage, accounts

# testing has 3 categories: arrange, act and assert
# arranging is like initialization
# act is do what u want to actually test
# assert is check if what u did matches what u wanted to do


def test_deploy():
    # arrange
    account = accounts[0]
    # act
    simple_storage = SimpleStorage.deploy({"from": account})
    start_value = simple_storage.retrieve()
    # assert
    expected = 0
    assert start_value == expected


def test_updating_storage():
    # arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # act
    expected = 15
    stored_value = simple_storage.store(expected, {"from": account})
    # assert
    assert expected == simple_storage.retrieve()


# to test just one function
# brownie test -k test_updating_storage
# brownie test --pdb (actually opens a python shell as a debugger if something is wrong to check the values )
