async function main() {
    const { execute } = deployments;
    const { deployer } = await getNamedAccounts();

    // markets
    const bHT  = '0xC6f65124FB5f9cF8F4F6aBad03f80B90Dcc28679';
    const bMDX = '0xB44aAAee673971F7AcAbE31993509067e631b64D';

    // 喂价
    await execute('SimplePriceOracle', { from: deployer }, 'setUnderlyingPrice', bHT, ethers.utils.parseUnits('20'));
    await execute('SimplePriceOracle', { from: deployer }, 'setUnderlyingPrice', bMDX, ethers.utils.parseUnits('3'));

    console.log('mock simple oracle set completed');
}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error);
        process.exit(1);
    });
