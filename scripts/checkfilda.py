
HBTC = '0x66a79d23e58475d2738179ca52cd0b41d73f0bea'
ETH = '0x64ff637fb478863b7468bc97d30a5bf3a428a1fd'
HUSD = '0x0298c2b32eae4da002a15f36fdf7615bea3da047'
USDT = '0xa71edc38d189767582c38a3145b5873052c3e47a'
WHT = '0x5545153ccfca01fbd7dd11c0b23ba694d9509a6f'
MDX = '0x25d2e80cb6b86881fd7e07dd263fb79f4abe033c'

FliDa_USDT_CToken = '0xaab0c9561d5703e84867670ac78f6b5b4b40a7c1'
FliDa_HUSD_CToken = '0xb16df14c53c4bcff220f4314ebce70183dd804c0'
FliDa_WHT_CToken = '0x824151251B38056d54A15E56B73c54ba44811aF8'
FliDa_HBTC_CToken = '0xf2a308d3aea9bd16799a5984e20fdbfef6c3f595'
FliDa_ETH_CToken =  '0x033f8c30bb17b47f6f1f46f3a42cc9771ccbcaae'
FliDa_HPT_CToken =  '0x749E0198f12559E7606987F8e7bD3AA1DE6d236E'  # 40%
FliDa_MDX_CToken =  '0x5788C014D41cA706DE03969E283eE7b93827B7B1'  # 50%

0xF2a308d3Aea9bD16799A5984E20FDBfEf6c3F595

Unitroller
0xb74633f2022452f377403b638167b0a135db096d

Comptroller
0xf9b7e5f27e95715be757a82116de54036a75c507

comp = Comptroller.at('0xb74633f2022452f377403b638167b0a135db096d')


ChainlinkAdaptor
0xA7042D87b25b18875cD1d2b1CE535C5488bc4Fd0

QsPriceOracleV2
0xCAffE113E75EFe0E12ac7A15d90B170726241B61


ETH = 2626480669582202241024

# FliDa_HPT_CToken ctoken 设定
# HPT 设置来源  0x1b7f7a8706D46C3D7cBB8DdDec472B9845Fe51E1
baseRatePerYear       = 0.02e18 #  ethers.utils.parseUnits('0.02'); # 年基础利率  == 0.03e18
multiplierPerYear     = 0.312e18 # ethers.utils.parseUnits('0.73');  # 同上起跳
jumpMultiplierPerYear = 7e18 # ethers.utils.parseUnits('3.1');
kink_                 = 0.95e18 # ethers.utils.parseUnits('0.55');

# BTC 设置来源 0xac1cF0b47088B72f8bD0f95D992565529Fad0faE
baseRatePerYear       = 0.05e18 #  ethers.utils.parseUnits('0.02'); # 年基础利率  == 0.03e18
multiplierPerYear     = 0.312e18 # ethers.utils.parseUnits('0.73');  # 同上起跳
jumpMultiplierPerYear = 5e18 # ethers.utils.parseUnits('3.1');
kink_                 = 0.95e18 # ethers.utils.parseUnits('0.55');


怎们自己的正式报价
0xD4a56436e64AEF094b09eb4E74bAF9893dc3f8aA


Channels_USDT_CToken = '0x3dA74C09ccb8faBa3153b7f6189dDA9d7F28156A'
Channels_HUSD_CToken = '0x9a57eAB16d371048c56cbE0c4D608096aEC5b405'
Channels_WHT_CToken = '0x397c6D1723360CC1c317CdC9B2E926Ae29626Ff3'
Channels_HBTC_CToken = '0x8feFb583e077de36F68444a14E68172b01e27dD7'
Channels_ETH_CToken =  '0x01371C08E2AE6F78D42c9796FA20DDb245Df3885'

Comptroller
0x8955aeC67f06875Ee98d69e6fe5BDEA7B60e9770

comp = Comptroller.at('0x8955aeC67f06875Ee98d69e6fe5BDEA7B60e9770')
>>> comp.oracle()
'0x1c3F7B75eE5025c36a83337E2969899622955256'
