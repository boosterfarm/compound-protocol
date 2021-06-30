const func = async ({ getNamedAccounts, deployments, network }) => {
    const { deploy, execute } = deployments;
    const { deployer } = await getNamedAccounts();

    // 部署账户
    const options = { from: deployer };

    // Comptroller Proxy
    const unitroller = await deploy('Unitroller', options);;

    // Comptroller Implementation
    const comptroller = await deploy('Comptroller', options);

    await execute('Unitroller', options, '_setPendingImplementation', comptroller.address);
    await execute('Comptroller', options, '_become', unitroller.address);

    console.log('1. Comptroller has deployed');
    return network.live;
  };

  func.id = 'deploy_comptroller';
  module.exports = func;
