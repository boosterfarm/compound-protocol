async function main() {
    const { deploy } = deployments;
    const { deployer } = await getNamedAccounts();

    // Deploy: 利率模型
    // Filda fMDX interest: https://hecoinfo.com/address/0x320cb3BaB9D9279672fB5c9B22F4e6113116d84b

    const baseRatePerYear       = ethers.utils.parseUnits('0.02');
    const multiplierPerYear     = ethers.utils.parseUnits('0.73');
    const jumpMultiplierPerYear = ethers.utils.parseUnits('3.1');
    const kink_                 = ethers.utils.parseUnits('0.55');
    const owner_                = deployer;

    const model = await deploy('JumpRateModelV2', {
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

    console.log('interest rate model = %s', model.address);
}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error);
        process.exit(1);
    });
