async function main() {
    const { get } = deployments;
    const signer = await ethers.getNamedSigner('deployer');

    const Comptroller = await get('Comptroller');
    const Unitroller  = await get('Unitroller');
    const unitroller  = await ethers.getContractAt(Comptroller.abi, Unitroller.address, signer);

    // markets
    const bHT  = '0xC6f65124FB5f9cF8F4F6aBad03f80B90Dcc28679';
    const bMDX = '0xB44aAAee673971F7AcAbE31993509067e631b64D';

    // Price Oracle
    const oracle = '0xe720B11c1333B2733E5050085142bc4C4cD9574c';

    // 1. _setPriceOracle
    await unitroller._setPriceOracle(oracle);

    // 2. _setCloseFactor: 每次最大清算比例 50%
    await unitroller._setCloseFactor(ethers.utils.parseUnits('0.5'));

    // 3. _setLiquidationIncentive: 清算时相当于 9折 购买抵押币
    await unitroller._setLiquidationIncentive(ethers.utils.parseUnits('1.1'));

    // 3. _supportMarket
    await unitroller._supportMarket(bHT);
    await unitroller._supportMarket(bMDX);

    // // 4. _setCompSpeed: 0 = 没有平台币奖励
    // await unitroller._setCompSpeed(cMDX, 0);

    // 5. _setCollateralFactor: 最大抵押比例
    await unitroller._setCollateralFactor(bHT, ethers.utils.parseUnits('0.8'));
    await unitroller._setCollateralFactor(bMDX, ethers.utils.parseUnits('0.5'));

    // // 6. _setMarketBorrowCaps: 每个 market 最大借款限额
    // await unitroller._setMarketBorrowCaps([ /* markets */ ], [ /* 最大借款限数量 */ ])

    // // 7. _setSupplyWhitlist: 设置存款白名单
    // await unitroller._setSupplyWhitlist(存款用户, true or false);
    await unitroller._setSupplyWhitlist('0x2EB83949a5a7C78D72e52Edb15387C442023AeA8', true);
    await unitroller._setSupplyWhitlist('0xBad7CB63a36EFDC1c98D438F00904441C0C3E281', true);

    // // 8. _setLiquidateWhitlist: 清算白名单
    // await unitroller._setLiquidateWhitlist(借款人, 清算人);

    // 9. _setCompAddress: 设置平台币
    // await unitroller._setCompAddress(`token address`)

    console.log('set controller attributes');
}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error);
        process.exit(1);
    });
