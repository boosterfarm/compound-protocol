
#!/usr/bin/python3


from brownie import *
import time

network.main.gas_buffer(2)

root = '888a68797b8c0721b79dd74e30a697a890b8e3ab84f0c5c6c76cec6118402222'
acct = accounts.add(root)

# temp = 'f6767b9f5ec19490478f38ec45fc6117576ddab1be5e731f6932399da39e6632'
# tempacct = accounts.add(temp)
# tempacct.transfer(acct, tempacct.balance()-21000*100e10)

HBTC = '0x66a79d23e58475d2738179ca52cd0b41d73f0bea'
ETH = '0x64ff637fb478863b7468bc97d30a5bf3a428a1fd'
HUSD = '0x0298c2b32eae4da002a15f36fdf7615bea3da047'
USDT = '0xa71edc38d189767582c38a3145b5873052c3e47a'
WHT = '0x5545153ccfca01fbd7dd11c0b23ba694d9509a6f'
MDX = '0x25d2e80cb6b86881fd7e07dd263fb79f4abe033c'
SLNV2 = '0x4e252342cf35ff02c4cca9bc655129f5b4a2f901'
FILDA = '0xe36ffd17b2661eb57144ceaef942d95295e637f0'
HPT = '0xe499ef4616993730ced0f31fa2703b92b50bb536'
LHB = '0x8f67854497218043e1f72908ffe38d0ed7f24721'
YFI = '0xb4f019beac758abbee2f906033aaa2f0f6dacb35'
HFIL= '0xae3a768f9ab104c69a7cd6041fe16ffa235d1810'
BXH = '0xcbd6cb9243d8e3381fea611ef023e17d1b7aedf0'
AAVE = '0x202b4936fe1a82a4965220860ae46d7d3939bb25'
UNI = '0x22c54ce8321a4015740ee1109d9cbc25815c46e6'
HBCH = '0xef3cebd77e0c52cb6f60875d9306397b5caca375'
SNX = '0x777850281719d5a96c29812ab72f822e0e09f3da'
HDOT = '0xa2c49cee16a5e5bdefde931107dc1fae9f7773e3'
HLTC = '0xecb56cf772b5c9a6907fb7d32387da2fcbfb63b4'

FDOT = '0xAfb9c2334AF17F362fFcaB0BA3B02286474724e7'
FBXH = '0xfB8409481f2a81222CAe7157F7D1fc343850f9Fc'
FUSDC = '0x39B43b8aE5bEf016AffcF936c915Df09CC114cb7'

unitroller = None
comptroller = None
priceoracle = None
ethercToken = None
ethermax = None

# unitroller = Unitroller.at("0x0572F7d63E031ee7461E5813b5a62f35cA081332")
# comptroller = Comptroller.at("0x927B467B5c0De783491cb232696edbB185399652")
# priceoracle = SimplePriceOracle.at("0xa2FDF734A3bed591D35FF8d9701e7D4a1b44daAb")
# tokenlist =  [<CErc20Delegator Contract '0x19962570fed7fA615779dE0e66E078D1d1a92D95'>, <CErc20Delegator Contract '0x5e857d90A4b8ffD89bE686200D648eB3649Ff650'>, <CErc20Delegator Contract '0x1fD171d9DE75D622B7c706835dc35dD48CC7440F'>]
# getAssetsIn ('0x19962570fed7fA615779dE0e66E078D1d1a92D95', '0x5e857d90A4b8ffD89bE686200D648eB3649Ff650', '0x1fD171d9DE75D622B7c706835dc35dD48CC7440F')

if 1:
    pass
    # unitroller = Unitroller.at('0xaF6d82Da857AEf1b54E41abbaB4961ED98e8BC99')
    # comptroller = Comptroller.at('0xcd134F8468ace8F362316997b2b9923fB62bDb79')
    # priceoracle = SimplePriceOracle.at('0x7479F3d91A4085662EA16b37CfE3a271a1Cd8dd4')
    # tokendot = CErc20Delegator.at('0xE5DA383358e0314550ebd8FB9d3cCae7AF4a7035')
    # tokenbxh = CErc20Delegator.at('0x225e7C74e1312e13b2914d461602A895f83a20b8')
    # unitroller = Unitroller.at('0x212d46F1579fa2Ed50879138ccf34146C48c4426')
    # comptroller = Comptroller.at('0xf17765D043DB8BA3951d736a48D6C171b96E55E6')
    # priceoracle = SimplePriceOracle.at('0x6704b177a043938323977EB9c766bC7125aD07b0')
    # unitroller = Unitroller.at('0x1c35228ef41aDDE6921Fd5ef1570C5e59088f882')
    # comptroller = Comptroller.at('0x1AA477652c6125e74d1f564edf9c0F16e1D1074B')
    # priceoracle = SimplePriceOracle.at('0x516E969754cD01eD515Abf648B2E6531EF4956cF')
    
def deploy_001_comptroller(deployer):
    global unitroller
    global comptroller
    # Comptroller Proxy
    if unitroller is None:
        unitroller = Unitroller.deploy({'from':deployer})
    if comptroller is None:
        comptroller = Comptroller.deploy({'from':deployer})

    unitroller._setPendingImplementation(comptroller.address, {'from':deployer})
    comptroller._become(unitroller.address, {'from':deployer})

def deploy_002_price_oracle(deployer):
    global priceoracle
    if priceoracle is None:
        priceoracle = MultiSourceOracle.deploy({'from':deployer})
    return priceoracle

def deploy_001_deploy_oracle(deployer):
    # // markets
    global priceoracle

    # // 喂价
    priceoracle.setPrices([FDOT,FBXH,FUSDC], [15e18, 0.5e18, 1e18], {'from':deployer})
    # priceoracle.setDirectPrice(MDX, 3e18, {'from':deployer})
    # priceoracle.setDirectPrice(USDT, 1e18, {'from':deployer})

# 002_deploy_rate_model  pass 

def deploy_003_deploy_ht(deployer):
    global ethercToken
    global ethermax

    # // Deploy: 利率模型
    # // Filda fHT interest: https://hecoinfo.com/address/0xC57f9a9127093EAFdB6405349DD4C0C0Fc180e8f

    baseRatePerYear       = 0.02e18 # ethers.utils.parseUnits('0.02');  年基础利率
    multiplierPerYear     = 0.32e18 # ethers.utils.parseUnits('0.32');  利率逐年递增系数？
    jumpMultiplierPerYear = 5e18 # ethers.utils.parseUnits('5');        利率起跳点
    kink_                 = 0.95e18 # ethers.utils.parseUnits('0.95');  同上起跳
    owner_                = deployer

    ratemodel = JumpRateModelV2.deploy(baseRatePerYear, multiplierPerYear, 
                            jumpMultiplierPerYear, kink_, owner_, {'from': deployer})

    # const interestRateModel = await deploy('JumpRateModelV2', {
    #     from: deployer,

    #     // 利率参数
    #     args: [
    #         baseRatePerYear,
    #         multiplierPerYear,
    #         jumpMultiplierPerYear,
    #         kink_,
    #         owner_
    #     ]
    # });

    # // bHT: 初始化参数
    # const comptroller = '0x1994D56Cf84AEa1adfBFB63EC04cB200A380fe5c';
    initialExchangeRateMantissa = 0.02e18 # ethers.utils.parseUnits('0.02'); 初始 bHT  和 HT 兑换率
    name = 'Booster HT'
    symbol = 'bHT'
    decimals = 18
    admin = deployer

    if ethercToken is None:
        ethercToken = CEther.deploy(unitroller, ratemodel, initialExchangeRateMantissa, 
                        name, symbol, decimals, admin, {'from': deployer})

    # CEther。

    # // Deploy: cToken
    # const bHT = await deploy('CEther', {
    #     from: deployer,

    #     args: [
    #         comptroller,
    #         interestRateModel.address,
    #         initialExchangeRateMantissa,
    #         name,
    #         symbol,
    #         decimals,
    #         admin
    #     ]
    # });

    # // // 1. _setPendingAdmin
    # // await bHT._setPendingAdmin(address newAdmin);

    # // // 1.1 _acceptAdmin
    # // await bHT._acceptAdmin().send({ from: `newAdmin`});

    # // // 2. _setComptroller
    # // await bHT._setComptroller(address);

    # // // 3. _setInterestRateModel
    # // await bHT._setInterestRateModel(address);

    # // 4. _setReserveFactor: 储备金率
    # await bHT._setReserveFactor(ethers.utils.parseUnits('0.15'));
    ethercToken._setReserveFactor(0.01e18, {'from': deployer})

    if ethermax is None:
        ethermax = Maximillion.deploy(ethercToken, {'from': deployer})

    # // Deploy: repay max debt // ht 特有， 每次获取最大可提取？
    # const max = await deploy('Maximillion', {
    #     from: deployer,
    #     args: [ bHT.address ]
    # });
    return ethercToken

def deploy_004_deploy_erc20(deployer, underlying, name, symbol):
    global unitroller
    global interestRateModel
    global priceoracle

# if 1:
    baseRatePerYear       = 0.02e18 #  ethers.utils.parseUnits('0.02'); # 年基础利率
    multiplierPerYear     = 0.73e18 # ethers.utils.parseUnits('0.73');  # 同上起跳
    jumpMultiplierPerYear = 3.1e18 # ethers.utils.parseUnits('3.1');
    kink_                 = 0.55e18 # ethers.utils.parseUnits('0.55');
    owner_                = deployer
    erc20RateModel = JumpRateModelV2.deploy(baseRatePerYear, multiplierPerYear, 
                            jumpMultiplierPerYear, kink_, owner_, {'from': deployer})

    # erc20RateModel = await deploy('JumpRateModelV2', {
    #     from: deployer,

    #     // 利率参数
    #     args: [
    #         baseRatePerYear,
    #         multiplierPerYear,
    #         jumpMultiplierPerYear,
    #         kink_,
    #         owner_
    #     ]
    # });

    # console.log('interest rate model = %s', model.address);

    # // MDX
    # const underlying = '0x25D2e80cB6B86881Fd7e07dd263Fb79f4AbE033c';
    # comptroller = unitroller
    # interestRateModel = erc20RateModel

    initialExchangeRateMantissa = 0.02e18 # ethers.utils.parseUnits('0.02');
    # const name = 'Booster MDX';
    # const symbol = 'bMDX';
    decimals = 18
    admin = deployer
    # const implementation = await deploy('CErc20Delegate', { from: deployer });
    # const becomeImplementationData = Buffer.alloc(0);

    implementation = CErc20Delegate.deploy({ 'from': deployer })

    print('underlying', interface.ERC20(underlying).symbol(), interface.ERC20(underlying).name())

    ctoken = CErc20Delegator.deploy(underlying, unitroller, erc20RateModel, initialExchangeRateMantissa,
                name, symbol, decimals, admin, implementation, b'', { 'from': deployer, 'gas_limit':300e4})

    # // Deploy delegator
    # const bToken = await deploy('CErc20Delegator', {
    #     from: deployer,

    #     args: [
    #         underlying,
    #         comptroller,
    #         interestRateModel,
    #         initialExchangeRateMantissa,
    #         name,
    #         symbol,
    #         decimals,
    #         admin,
    #         implementation.address,
    #         becomeImplementationData
    #     ]
    # });

    ctoken._setReserveFactor(0.05e18, { 'from': deployer })

    # // // 1. _setPendingAdmin
    # // await bToken._setPendingAdmin(address newAdmin);

    # // // 1.1 _acceptAdmin
    # // await bToken._acceptAdmin().send({ from: `newAdmin`});

    # // // 2. _setComptroller
    # // await bToken._setComptroller(address);

    # // // 3. _setInterestRateModel
    # // await bToken._setInterestRateModel(address);

    # // 4. _setReserveFactor: 储备金率
    # await bToken._setReserveFactor(ethers.utils.parseUnits('0.15'));

    # // // 5. _addReserves: 增加储备金
    # // await bToken._addReserves(uint)

    # // // 6. _reduceReserves: 减少储备金到 admin 账户(需要 admin 权限)
    # // await bToken._reduceReserves(uint)

    # console.log('bMDX delegator      = %s', bToken.address);
    # console.log('bMDX implementation = %s', implementation.address);
    # console.log('bMDX has deployed');

    # 0x59666d1A521f46EA02E8d29BA2cF80F75ecB31FA
    print('ctoken', ctoken, 'settingz')
    assert(unitroller != None)
    comptr = interface.IComptrollerControl(unitroller.address)
    comptr._supportMarket(ctoken, { 'from': deployer, 'gas_limit':300e4})
    comptr._setCompSpeed(ctoken, 0, { 'from': deployer, 'gas_limit':300e4})
    comptr._setSupplyWhitlist(deployer, True, { 'from': deployer })
    priceoracle.setUnderlyingPrice(ctoken, 1e18, { 'from': acct })
    comptr._setCollateralFactor(ctoken, 0.97e18, { 'from': deployer, 'gas_limit':300e4})
    print('ctoken-marketsinfo', ctoken, comptr.markets(ctoken))
    return ctoken


def deploy_006_set_attributes(deployer):
    global unitroller
    global priceoracle
    comptr = interface.IComptrollerControl(unitroller.address)

    # // 1. _setPriceOracle
    # await unitroller._setPriceOracle(oracle);
    comptr._setPriceOracle(priceoracle, { 'from': deployer })

    # // 2. _setCloseFactor: 每次最大清算比例 50%
    # await unitroller._setCloseFactor(ethers.utils.parseUnits('0.5'));
    comptr._setCloseFactor(0.5e18, { 'from': deployer })

    # // 3. _setLiquidationIncentive: 清算时相当于 9折 购买抵押币
    # await unitroller._setLiquidationIncentive(ethers.utils.parseUnits('1.1'));
    comptr._setLiquidationIncentive(1.1e18, { 'from': deployer })

    # // 3. _supportMarket
    # await unitroller._supportMarket(bHT);
    # await unitroller._supportMarket(bMDX);
    # for i in ctokenlist:
    #     comptr._supportMarket(i, { 'from': deployer }) 
    #     comptr._setCompSpeed(i, 0, { 'from': deployer }) 
    #     comptr._setCollateralFactor(i, 0.97e18, { 'from': deployer })

    # comptr.enterMarkets(ctokenlist, { 'from': deployer })


    comptr._setSupplyWhitlist(deployer, True, { 'from': deployer })
    comptr._setLiquidateWhitlist(deployer, deployer, { 'from': deployer })


    # // // 4. _setCompSpeed: 0 = 没有平台币奖励
    # // await unitroller._setCompSpeed(cMDX, 0);
    # comptroller._setCompSpeed(cMDX, 0);

    # // 5. _setCollateralFactor: 最大抵押比例
    # await unitroller._setCollateralFactor(bHT, ethers.utils.parseUnits('0.8'));
    # await unitroller._setCollateralFactor(bMDX, ethers.utils.parseUnits('0.5'));

    # // // 6. _setMarketBorrowCaps: 每个 market 最大借款限额, 绝对值
    # // await unitroller._setMarketBorrowCaps([ /* markets */ ], [ /* 最大借款限数量 */ ])

    # // // 7. _setSupplyWhitlist: 设置存款白名单
    # // await unitroller._setSupplyWhitlist(存款用户, true or false);
    # await unitroller._setSupplyWhitlist('0x2EB83949a5a7C78D72e52Edb15387C442023AeA8', true);
    # await unitroller._setSupplyWhitlist('0xBad7CB63a36EFDC1c98D438F00904441C0C3E281', true);

    # // // 8. _setLiquidateWhitlist: 清算白名单
    # // await unitroller._setLiquidateWhitlist(借款人, 清算人);

    # // 9. _setCompAddress: 设置平台币
    # // await unitroller._setCompAddress(`token address`)
def test_mint_redeem(acct, ctoken):
    # ctoken = CErc20Delegator.at(comptr.getAssetsIn(acct)[0])
    global unitroller
    comptr = interface.IComptrollerControl(unitroller.address)
    comptr.enterMarkets([ctoken], { 'from': acct, 'gas_limit':300e4})
    print('getAssetsIn', comptr.getAssetsIn(acct))
    for i in comptr.getAssetsIn(acct):
        print('marketsinfo', i, comptr.markets(i))
        # comptr._setCollateralFactor(i, 0.97e18, { 'from': deployer, 'gas_limit':300e4})

    basetoken = interface.ERC20(ctoken.underlying())
    print('test_mint_redeem', ctoken.symbol(), basetoken.symbol(), basetoken.balanceOf(acct))
    basetoken.approve(ctoken, '0x'+'f'*40, { 'from': acct })
    supply = 100e18
    borrow = 95e18
    ctoken.mint(supply, { 'from': acct })
    print('ctoken supply', ctoken.totalSupply() * ctoken.exchangeRateStored()/1e18)
    print('getHypotheticalAccountLiquidity', comptr.getHypotheticalAccountLiquidity(acct, ctoken, borrow, 0))
    c = ctoken.borrow(borrow, { 'from': acct })
    print('borrow', c.info())
    c = ctoken.borrowBalanceCurrent(acct, { 'from': acct })
    print('borrowBalanceCurrent', c.info())
    ctoken.repayBorrow(borrow, { 'from': acct })
    ctoken.redeem(borrow, { 'from': acct })

def show_global_all(tokenlist):
    def printis(name, classname, instance):
        if instance is None:
            print('%s = None' % name)
            return
        print('%s = %s.at("%s")' % (name, classname, instance.address))
    
    printis('unitroller', 'Unitroller', unitroller)
    printis('comptroller', 'Comptroller', comptroller)
    printis('priceoracle', 'SimplePriceOracle', priceoracle)
    # printis('ethercToken', 'CEther', ethercToken)
    # printis('ethermax', 'Maximillion', ethermax)
    print('tokenlist = ', tokenlist)

# unitroller = Unitroller.at("0xF2c6e903894CD3192BCe2aB4a2962ACa886F3250")
# comptroller = Comptroller.at("0x552EbD15698b42bc0D2390990888DcFa5F1fb8cd")
# priceoracle = SimplePriceOracle.at("0x2E57Ac0C12F3e44509b829164302ae40eD832dc4")
# tokenlist = ['0xeeE009D27014baa2E2265fF2A38256D9581e4Ddb', '0x6c9dB03A7C226bdB060965A65a4501B91f94a65E', '0x5BdBc0977287A12761E7652fD47071c9c72Ed3b6']

def main():
    # 初始化环境
    print('developer', acct.address)

    # 仅仅测试
    global unitroller
    global comptroller
    global priceoracle
    global tokenlist
    
    # for idc in tokenlist:
    #     i = CErc20Delegator.at(idc)
    #     test_mint_redeem(acct, i)
    # # tokenlist =  [<CErc20Delegator Contract '0xeeE009D27014baa2E2265fF2A38256D9581e4Ddb'>, <CErc20Delegator Contract '0x6c9dB03A7C226bdB060965A65a4501B91f94a65E'>, <CErc20Delegator Contract '0x5BdBc0977287A12761E7652fD47071c9c72Ed3b6'>]
    # return 
    
    tokenlist = []
    deploy_001_comptroller(acct)
    priceoracle = deploy_002_price_oracle(acct)
    deploy_001_deploy_oracle(acct)
    show_global_all(tokenlist)

    deploy_006_set_attributes(acct)
    # ctokeneth = deploy_003_deploy_ht(acct)
    # tokenlist.append(ctokeneth)
    # underlying, name, symbol
    # global priceoracle
    assert(priceoracle != None)
    ctokendot = deploy_004_deploy_erc20(acct, FDOT, 'Booster FDOT', 'bHDOT')
    priceoracle.setUnderlyingPrice(ctokendot, 120e18, { 'from': acct })
    tokenlist.append(ctokendot)

    ctokenbxh = deploy_004_deploy_erc20(acct, FBXH, 'Booster FBXH', 'bBXH')
    priceoracle.setUnderlyingPrice(ctokenbxh, 2.5e18, { 'from': acct })
    tokenlist.append(ctokenbxh)

    ctokenusdc = deploy_004_deploy_erc20(acct, FUSDC, 'Booster FUSDC', 'bUSDC')
    priceoracle.setUnderlyingPrice(ctokenusdc, 1e18, { 'from': acct })
    tokenlist.append(ctokenusdc)

    for i in tokenlist:
        assert(priceoracle.getUnderlyingPrice(i) > 0)

    show_global_all(tokenlist)

    # FDOT = '0xAfb9c2334AF17F362fFcaB0BA3B02286474724e7'
    # FBXH = '0xfB8409481f2a81222CAe7157F7D1fc343850f9Fc'
    # FUSDC = '0x39B43b8aE5bEf016AffcF936c915Df09CC114cb7'

    for i in tokenlist:
        test_mint_redeem(acct, i)
    # test_mint_redeem(acct, ctokenbxh)
    # test_mint_redeem(acct, ctokenusdc)
    return 
