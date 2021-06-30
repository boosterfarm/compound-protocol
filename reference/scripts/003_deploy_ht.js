async function main() {
    const { deploy } = deployments;
    const { deployer } = await getNamedAccounts();

    // Deploy: 利率模型
    // Filda fHT interest: https://hecoinfo.com/address/0xC57f9a9127093EAFdB6405349DD4C0C0Fc180e8f

    const baseRatePerYear       = ethers.utils.parseUnits('0.02');
    const multiplierPerYear     = ethers.utils.parseUnits('0.32');
    const jumpMultiplierPerYear = ethers.utils.parseUnits('5');
    const kink_                 = ethers.utils.parseUnits('0.95');
    const owner_                = deployer;

    const interestRateModel = await deploy('JumpRateModelV2', {
        from: deployer,

        // 利率参数
        args: [
            baseRatePerYear,
            multiplierPerYear,
            jumpMultiplierPerYear,
            kink_,
            owner_
        ]
    });

    // bHT: 初始化参数
    const comptroller = '0x1994D56Cf84AEa1adfBFB63EC04cB200A380fe5c';
    const initialExchangeRateMantissa = ethers.utils.parseUnits('0.02');
    const name = 'Booster HT';
    const symbol = 'bHT';
    const decimals = 18;
    const admin = deployer;

    // Deploy: cToken
    const bHT = await deploy('CEther', {
        from: deployer,

        args: [
            comptroller,
            interestRateModel.address,
            initialExchangeRateMantissa,
            name,
            symbol,
            decimals,
            admin
        ]
    });

    // // 1. _setPendingAdmin
    // await bHT._setPendingAdmin(address newAdmin);

    // // 1.1 _acceptAdmin
    // await bHT._acceptAdmin().send({ from: `newAdmin`});

    // // 2. _setComptroller
    // await bHT._setComptroller(address);

    // // 3. _setInterestRateModel
    // await bHT._setInterestRateModel(address);

    // 4. _setReserveFactor: 储备金率
    await bHT._setReserveFactor(ethers.utils.parseUnits('0.15'));

    // Deploy: repay max debt // ht 特有， 每次
    const max = await deploy('Maximillion', {
        from: deployer,
        args: [ bHT.address ]
    });

    console.log('bHT market         = %s', bHT.address);
    console.log('bHT interest model = %s', interestRateModel.address);
    console.log('bHT maximillion    = %s', max.address);
    console.log('bHT has deployed');
}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error);
        process.exit(1);
    });
