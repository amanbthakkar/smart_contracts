//SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    uint256 favoriteNumber; //internal and initialized to 0 as default
    bool favoriteSomething;

    //create a struct for People

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People[] people; //datatype< >visibility< >name

    function store(uint256 _favorite_number) public returns (uint256) {
        favoriteNumber = _favorite_number;
        return favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
    }
}
