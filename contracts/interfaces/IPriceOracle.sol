// SPDX-License-Identifier: MIT

pragma solidity 0.5.16;

pragma experimental ABIEncoderV2;

interface IPriceOracle {

    function setPrices(
        address[] calldata tokens,
        uint[] calldata prices
    ) external;

    function getPrice(address _token) external view returns (int);
    function getUnderlyingPrice(address cToken) external view returns (uint);
}
