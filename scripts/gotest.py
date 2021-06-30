
#!/usr/bin/python3


from brownie import *
import time

root = '888a68797b8c0721b79dd74e30a697a890b8e3ab84f0c5c6c76cec6118402222'
acct = accounts.add(root)

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

unitroller = None
comptroller = None
priceoracle = None
ethercToken = None
ethermax = None

if 1:
    unitroller = Unitroller.at('0xCd4BD5C47Cbf6fA93f52C539CC13971Ad2294B57')
    comptroller = Comptroller.at('0xF3D9db5Aed82038720f611b2d95D8AB429C1b2A0')
    priceoracle = SimplePriceOracle.at('0xCF99d29ac8d84F9a49794Be0a9Db7BC07eb09085')
    ethercToken = CEther.at('0x97Aa04a71DF209C80F3e8A0F5aa854d386771973')
    ethermax = Maximillion.at('0xC38eEFE140fCb508161d4138F498C530774e4021')
    tokenbxh = CErc20Delegator.at('0xFEcc0a44Cc81EbC27BDCE261DE96B999530Ba83a')
    tokendot = CErc20Delegator.at('0x33e57EC419F722D9E3C4253B1058519d6Fc14A98')
    comptr = interface.IComptrollerControl(unitroller.address)

unitroller = Unitroller.at(0xCd4BD5C47Cbf6fA93f52C539CC13971Ad2294B57)
comptroller = Comptroller.at(0xF3D9db5Aed82038720f611b2d95D8AB429C1b2A0)
priceoracle = SimplePriceOracle.at(0xCF99d29ac8d84F9a49794Be0a9Db7BC07eb09085)
tokenlist =  [<CErc20Delegator Contract '0xFEcc0a44Cc81EbC27BDCE261DE96B999530Ba83a'>, <CErc20Delegator Contract '0x33e57EC419F722D9E3C4253B1058519d6Fc14A98'>]
priceoracle.setUnderlyingPrice(tokendot, 120e18, { 'from': acct })
priceoracle.setUnderlyingPrice(tokenbxh, 2.5e18, { 'from': acct })

comptr._setCollateralFactor(tokendot, 0.97e18, { 'from': acct })
comptr.enterMarkets([tokenbxh, tokendot], { 'from': acct })
comptr.getAssetsIn(acct)
tokendot.borrow(9e5,  { 'from': acct })

def test_deposit(ctoken, acct):
    interface.ERC20(ctoken.underlying()).approve(ctoken, '0x'+'f'*40, { 'from': acct })
    tokendot.mint(1e6, { 'from': acct })
    tokendot.totalSupply() * tokendot.exchangeRateStored()/1e18

    c = tokendot.borrow(9e5, { 'from': acct })
    c = tokendot.borrowBalanceCurrent(acct, { 'from': acct })
    c.info()
    tokendot.repayBorrow(9e5, { 'from': acct })
    tokendot.redeem(55000000-100*5, { 'from': acct })
    

def deploy_006_set_attributes(deployer, ctokenlist):
    global comptroller
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
    # 设置支持市场，产币数量，抵押系数
    for i in ctokenlist:
        comptr._supportMarket(i, { 'from': deployer }) 
        comptr._setCompSpeed(i, 0, { 'from': deployer }) 
        comptr._setCollateralFactor(i, 0.97e18, { 'from': deployer })
    # 7. _setSupplyWhitlist: 设置存款白名单
    comptr._setSupplyWhitlist(deployer, True, { 'from': deployer })
    # 8. _setLiquidateWhitlist: 清算白名单
    comptr._setLiquidateWhitlist(deployer, deployer, { 'from': deployer })
    
    # tokendot._setComptroller(unitroller, { 'from': acct })

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


def show_global_all(tokenlist):
    def printis(name, classname, instance):
        if instance is None:
            print('%s = None' % name)
            return
        print('%s = %s.at(%s)' % (name, classname, instance.address))
    
    printis('unitroller', 'Unitroller', unitroller)
    printis('comptroller', 'Comptroller', comptroller)
    printis('priceoracle', 'SimplePriceOracle', priceoracle)
    printis('ethercToken', 'CEther', ethercToken)
    printis('ethermax', 'Maximillion', ethermax)
    print('tokenlist = ', tokenlist)

def main():
    # 初始化环境
    print('developer', acct.address)
    
    tokenlist = []
    deploy_001_comptroller(acct)
    deploy_002_price_oracle(acct)
    deploy_001_deploy_oracle(acct)
    show_global_all(tokenlist)

    # ctokeneth = deploy_003_deploy_ht(acct)
    # tokenlist.append(ctokeneth)
    # underlying, name, symbol
    ctokendot = deploy_004_deploy_erc20(acct, HDOT, 'Booster HDOT', 'bHDOT')
    tokenlist.append(ctokendot)
    ctokenbxh = deploy_004_deploy_erc20(acct, BXH, 'Booster BXH', 'bBXH')
    tokenlist.append(ctokenbxh)
    show_global_all(tokenlist)

    deploy_006_set_attributes(acct, tokenlist)
    return 
