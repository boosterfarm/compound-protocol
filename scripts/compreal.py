
#!/usr/bin/python3


from brownie import *
import time

network.main.gas_buffer(2)

root = '619c8c0a533c423c14a4bd4ee8891a05431508c14d902409cf59595dffca3d2f'
acct = accounts.add(root) # 0xBbf77cE5D1FDAD046E85157eE8b1Ab5796d1D99b

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

# FBTC = '0x8D34803d43f09614C4AFE9f83AaE7754eFf8214e'
# FBXH = '0xfB8409481f2a81222CAe7157F7D1fc343850f9Fc'
# FUSDC = '0x39B43b8aE5bEf016AffcF936c915Df09CC114cb7'

unitroller = None
comptroller = None
priceoracle = None
ethercToken = None

# MultiSourceOracle
priceoracle = interface.IPriceOracle("0x10c25F587E9826B5F7BDce7C337291a55CB6fA12")

if 1:
    # priceoracle = TokenOracle.at("0x10c25F587E9826B5F7BDce7C337291a55CB6fA12")
    unitroller = Unitroller.at("0x9D673D51592a0aC13562a4b6f5a3Dc01A6a4b230")
    comptroller = Comptroller.at("0x0cEA042368c0E510819CaD59269394C6c32f7779")
    bmdxctoken = CErc20Delegator.at("0x8A175FcD02CE66bE055b73e085F014fc5D268B79")
    bhptctoken = CErc20Delegator.at("0x63D65F2b6B1f2F468DA6CCB1f82cb041f9c2c20E")

def deploy_comptroller(deployer):
    global unitroller
    global comptroller
    # Comptroller Proxy
    if unitroller is None:
        unitroller = Unitroller.deploy({'from':deployer})
    if comptroller is None:
        comptroller = Comptroller.deploy({'from':deployer})

    unitroller._setPendingImplementation(comptroller.address, {'from':deployer})
    comptroller._become(unitroller.address, {'from':deployer})

    comptr = interface.IComptrollerControl(unitroller.address)

    # // 1. _setPriceOracle
    comptr._setPriceOracle(priceoracle, { 'from': deployer })
    # // 2. _setCloseFactor: 每次最大清算比例 50%
    comptr._setCloseFactor(0.5e18, { 'from': deployer })
    # // 3. _setLiquidationIncentive: 清算时相当于 9折 购买抵押币
    comptr._setLiquidationIncentive(1.1e18, { 'from': deployer })
    # comptr._setSupplyWhitlist(deployer, True, { 'from': deployer })
    comptr._setLiquidateWhitlist(deployer, deployer, { 'from': deployer })

def add_ctoken_erc20(deployer, info):
    global unitroller
    global interestRateModel
    global priceoracle

    assert(unitroller != None)
    assert(info['baseRatePerYear'] > 1e12)
    assert(info['multiplierPerYear'] > 1e12)
    assert(info['jumpMultiplierPerYear'] > 1e12)
    assert(info['kink_'] > 1e12)
    assert(info['reserveFactor'] > 1e12)  # 储备金率
    assert(info['collateralFactor'] > 1e12)  # 储备金率
    assert(len(info['underlying']) > 10)
    assert(len(info['name']) > 3)
    assert(len(info['symbol']) >= 3)
    assert(priceoracle.getPrice(info['underlying']) > 0) # 有币价计算

    print('add', info['symbol'], 'underlying', interface.ERC20(info['underlying']).symbol(), interface.ERC20(info['underlying']).name(), priceoracle.getPrice(info['underlying'])/1e8)

    owner_ = deployer
    erc20RateModel = JumpRateModelV2.deploy(info['baseRatePerYear'], info['multiplierPerYear'], 
                            info['jumpMultiplierPerYear'], info['kink_'], owner_, {'from': deployer})

    initialExchangeRateMantissa = 0.02e18
    decimals = 18
    admin = deployer

    implementation = CErc20Delegate.deploy({ 'from': deployer })
    ctoken = CErc20Delegator.deploy(info['underlying'], unitroller, erc20RateModel, initialExchangeRateMantissa,
                info['name'], info['symbol'], decimals, admin, implementation, b'', { 'from': deployer})

    ctoken._setReserveFactor(info['reserveFactor'], { 'from': deployer })

    comptr = interface.IComptrollerControl(unitroller.address)
    comptr._supportMarket(ctoken, { 'from': deployer})
    comptr._setCompSpeed(ctoken, 0, { 'from': deployer})
    comptr._setCollateralFactor(ctoken, info['collateralFactor'], { 'from': deployer})
    print('ctoken-marketsinfo', ctoken, comptr.markets(ctoken))
    return ctoken

def show_global_all(tokenlist):
    def printis(name, classname, instance):
        if instance is None:
            print('%s = None' % name)
            return
        print('%s = %s.at("%s")' % (name, classname, instance.address))
    
    printis('priceoracle', 'TokenOracle', priceoracle)
    printis('unitroller', 'Unitroller', unitroller)
    printis('comptroller', 'Comptroller', comptroller)
    for i in tokenlist:
        printis('%sctoken'% (i.symbol().lower()), 'CErc20Delegator', i)

def test_mint_redeem(acct, ctoken):
    global unitroller
    comptr = interface.IComptrollerControl(unitroller.address)
    comptr._setSupplyWhitlist(acct, True, { 'from': acct })

    comptr.enterMarkets([ctoken], {'from': acct})
    print('getAssetsIn', comptr.getAssetsIn(acct))
    for i in comptr.getAssetsIn(acct):
        print('marketsinfo', i, comptr.markets(i))
        # comptr._setCollateralFactor(i, 0.97e18, { 'from': deployer, 'gas_limit':300e4})
    basetoken = interface.ERC20(ctoken.underlying())
    print('test_mint_redeem', ctoken.symbol(), basetoken.symbol(), basetoken.balanceOf(acct))
    basetoken.approve(ctoken, '0x'+'f'*40, { 'from': acct })
    supply = 0.01e18
    borrow = 0.005e18
    ctoken.mint(supply, { 'from': acct })
    print('ctoken supply', ctoken.totalSupply() * ctoken.exchangeRateStored()/1e18)
    print('getHypotheticalAccountLiquidity', comptr.getHypotheticalAccountLiquidity(acct, ctoken, borrow, 0))
    c = ctoken.borrow(borrow, { 'from': acct })
    print('borrow', c.info())
    c = ctoken.borrowBalanceCurrent(acct, { 'from': acct })
    print('borrowBalanceCurrent', c.info())
    ctoken.repayBorrow(borrow, { 'from': acct })
    ctoken.redeem(int(supply*0.9999), { 'from': acct })

def main():
    # 初始化环境
    print('developer', acct.address)

    deploy_comptroller(acct)

    ctokenlist = []

    # // Deploy: 利率模型
    # // Filda fHT interest: https://hecoinfo.com/address/0xC57f9a9127093EAFdB6405349DD4C0C0Fc180e8f

    # price = priceoracle.getPrice(MDX) / 1e8
    # print(interface.ERC20(MDX).symbol(), price)
    # assert(price > 0)

    # ctokenInfo = {}
    # ctokenInfo['name'] = 'booster MDX'
    # ctokenInfo['symbol'] = 'bMDX'
    # ctokenInfo['underlying'] = MDX
    # ctokenInfo['baseRatePerYear'] =  0.03e18 # 年基础利率
    # ctokenInfo['multiplierPerYear'] = 0.73e18 # 利率逐年递增系数？
    # ctokenInfo['jumpMultiplierPerYear'] = 3.1e18 # 利率起跳点
    # ctokenInfo['kink_'] = 0.55e18              # 同上起跳 这个基本固定
    # ctokenInfo['reserveFactor'] = 0.8e18    # 储备金率
    # ctokenInfo['collateralFactor'] = 0.9e18  # 最大抵押比例

    # ctokennew = add_ctoken_erc20(acct, ctokenInfo)
    # ctokenlist.append(ctokennew)

    price = priceoracle.getPrice(HPT) / 1e8
    print(interface.ERC20(HPT).symbol(), price)
    assert(price > 0)

    ctokenInfo = {}
    ctokenInfo['name'] = 'booster HPT'
    ctokenInfo['symbol'] = 'bHPT'
    ctokenInfo['underlying'] = HPT
    ctokenInfo['baseRatePerYear'] =  0.32e18 # 年基础利率
    ctokenInfo['multiplierPerYear'] = 0.03e18 # 利率逐年递增系数？
    ctokenInfo['jumpMultiplierPerYear'] = 7e18 # 利率起跳点
    ctokenInfo['kink_'] = 0.95e18              # 同上起跳 这个基本固定
    ctokenInfo['reserveFactor'] = 0.8e18       # 储备金率
    ctokenInfo['collateralFactor'] = 0.9e18    # 最大抵押比例

    ctokennew = add_ctoken_erc20(acct, ctokenInfo)
    ctokenlist.append(ctokennew)

    show_global_all(ctokenlist)

    test_mint_redeem(acct, ctokennew)

    # show_global_all(ctokenlist)
