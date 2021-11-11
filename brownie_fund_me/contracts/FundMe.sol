// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

//cant run brownie compile here directly
//remix knows @chainlink/ is an npm package it can import from
//brownie does not know that. but it does know about github.
//tell brownie where to download 3rd party packages from - there is a package
//go to yaml file and add dependency
//now gotta tell brownie what is "@chainlink" also in yaml
//now after compiling, the build/ will have dependencies that are mentioned above!

contract FundMe {
    using SafeMathChainlink for uint256;
    //we want it to be able to accept payments so "payable"
    int256 public price_1;
    mapping(address => uint256) public funds;
    address[] public fundedBy;
    address owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed); //take this value in constructor at time of contract deployment itself
    }

    function fund() public payable {
        //record payments made to contract by some address
        uint256 minUSD = 50 * 10**18;
        require(
            getConversionRate(msg.value) >= minUSD,
            "Insufficient ETH spent!"
        ); //you want there to be some minumum ETH sent here
        funds[msg.sender] = msg.value; //funds is a mapping
        fundedBy.push(msg.sender); //since you cant iterate through the mapping gotta store the sender addresses
    }

    function getEntranceFee() public view returns (uint256) {
        //getPrice() returns price of 1 ETH in USD multiplied by 10^18
        uint256 minUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minUSD * precision) / price;
    }

    //use Oracle to convert funds to USD
    function getPrice() public view returns (uint256) {
        //AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        //above line commented out if already doing in constructor. initialized priceFeed globally!

        (, int256 price, , , ) = priceFeed.latestRoundData(); //gets price in USD with 8 decimal places
        //price_1 = price;// this is actual USD price * 10^8
        return uint256(price * 10000000000); //price in USD with 18 decimal places (divide by 10^18 to get USD price)
        //we cant send direct USD price because there are no decimals
        //the tutorial guy just likes to have everything in 18 decimal places because wei has 18
    }

    function getConversionRate(uint256 _ethSent) public view returns (uint256) {
        //_ethSent * price_per_eth = USD value
        //_ethSent * getConversionRate()/10^18 = USD value (check getConversionRate comments to know why)
        return uint256((_ethSent * getPrice()) / 1000000000000000000); //ie eth_sent * price per eth in USD ==> value of eth in USD
    }

    modifier onlyOwner() {
        //there can be a _; over here also but didn't yet get why
        require(msg.sender == owner);
        _; //code in function comes here
    }

    function withdrawAllFunds() public payable onlyOwner {
        //msg.sender HAS to be owner. either through require statement or through a modifier
        msg.sender.transfer(address(this).balance); //transfer this particular contract's balance to msg.sender

        //now clear funds from rest of accounts
        for (uint256 i = 0; i < fundedBy.length; i++) {
            funds[fundedBy[i]] = 0; //clear the mapping
        }
        //empty the array
        fundedBy = new address[](0);
    }
}
