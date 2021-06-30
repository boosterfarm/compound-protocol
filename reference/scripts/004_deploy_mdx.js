async function main() {
    const { deploy } = deployments;
    const { deployer } = await getNamedAccounts();

    // MDX
    const underlying = '0x25D2e80cB6B86881Fd7e07dd263Fb79f4AbE033c';
    const comptroller = '0x1994D56Cf84AEa1adfBFB63EC04cB200A380fe5c';
    const interestRateModel = '0x462808CeCb51803E0490Aeb2c2F24B0f542BeB26';

    const initialExchangeRateMantissa = ethers.utils.parseUnits('0.02');
    const name = 'Booster MDX';
    const symbol = 'bMDX';
    const decimals = 18;
    const admin = deployer;
    const implementation = await deploy('CErc20Delegate', { from: deployer });
    const becomeImplementationData = Buffer.alloc(0);

    // Deploy delegator
    const bToken = await deploy('CErc20Delegator', {
        from: deployer,

        args: [
            underlying,
            comptroller,
            interestRateModel,
            initialExchangeRateMantissa,
            name,
            symbol,
            decimals,
            admin,
            implementation.address,
            becomeImplementationData
        ]
    });

    // // 1. _setPendingAdmin
    // await bToken._setPendingAdmin(address newAdmin);

    // // 1.1 _acceptAdmin
    // await bToken._acceptAdmin().send({ from: `newAdmin`});

    // // 2. _setComptroller
    // await bToken._setComptroller(address);

    // // 3. _setInterestRateModel
    // await bToken._setInterestRateModel(address);

    // 4. _setReserveFactor: 储备金率
    await bToken._setReserveFactor(ethers.utils.parseUnits('0.15'));

    // // 5. _addReserves: 增加储备金
    // await bToken._addReserves(uint)

    // // 6. _reduceReserves: 减少储备金到 admin 账户(需要 admin 权限)
    // await bToken._reduceReserves(uint)

    console.log('bMDX delegator      = %s', bToken.address);
    console.log('bMDX implementation = %s', implementation.address);
    console.log('bMDX has deployed');
}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error);
        process.exit(1);
    });
