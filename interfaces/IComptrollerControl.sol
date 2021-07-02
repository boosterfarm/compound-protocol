pragma solidity ^0.5.16;

import "../contracts/CToken.sol";
import "../contracts/PriceOracle.sol";
// import "./ErrorReporter.sol";
// import "./ComptrollerInterface.sol";
// import "./ComptrollerStorage.sol";
// import "./Unitroller.sol";
// import "./Governance/Comp.sol";

interface IComptrollerControl {
    // 1. _setPriceOracle 设置爆仓价格查询
    function _setPriceOracle(PriceOracle newOracle) external returns (uint);
    // 2. _setCloseFactor: 每次最大清算比例 50%  => 0.5e18
    function _setCloseFactor(uint newCloseFactorMantissa) external returns (uint);
    // 3. _setLiquidationIncentive: 清算时相当于 9折 购买抵押币  => 1.1e18
    function _setLiquidationIncentive(uint newLiquidationIncentiveMantissa) external returns (uint);
    // 3. _supportMarket
    function _supportMarket(CToken cToken) external returns (uint);
    // 4. _setCompSpeed: 0 = 没有平台币奖励
    function _setCompSpeed(CToken cToken, uint compSpeed) external;
    // 5. _setCollateralFactor: 最大抵押比例
    function _setCollateralFactor(CToken cToken, uint newCollateralFactorMantissa) external returns (uint);
    // 6. _setMarketBorrowCaps: 每个 market 最大借款限额 => [ /* markets */ ], [ /* 最大借款限数量 */ ]
    function _setMarketBorrowCaps(CToken[] calldata cTokens, uint[] calldata newBorrowCaps) external;
    // 7. _setSupplyWhitlist: 设置存款白名单
    function _setSupplyWhitlist(address supplier, bool status) external;
    // 8. _setLiquidateWhitlist: 清算白名单 => 借款人, 清算人
    function _setLiquidateWhitlist(address borrower, address liquidator) external;
    function _setRepayBorrowWhitlist(address borrower, address repayer) external;
    function _setSeizeWhitlist(address borrower, address resizer) external;
    // 9. _setCompAddress: 设置平台币
    function _setCompAddress(address comp) external;

    // 允许抵押的市场
    function enterMarkets(address[] calldata cTokens) external returns (uint[] memory);
    function markets(address cTokens) external view returns (bool,uint,bool);

    function supplyWhitelist(address supplier) external view returns (bool);
    function liquidateWhitelist(address borrower) external view returns (bool);
    function borrowCaps(address cTokens) external view returns (uint);

    function getHypotheticalAccountLiquidity(
        address account,
        address cTokenModify,
        uint redeemTokens,
        uint borrowAmount) external view returns (uint, uint, uint);

    function getAssetsIn(address account) external view returns (address[] memory);

    function borrowAllowed(address cToken, address borrower, uint borrowAmount) external returns (uint);
}

