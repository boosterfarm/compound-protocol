const func = async ({ getNamedAccounts, deployments, network }) => {
    const { deploy } = deployments;
    const { deployer } = await getNamedAccounts();

    // 部署账户
    const options = { from: deployer };
    await deploy('SimplePriceOracle', options);

    console.log('2. Oracle has deployed');
    return network.live;
  };

  func.id = 'deploy_oracle';
  module.exports = func;
