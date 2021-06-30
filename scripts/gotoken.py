
#!/usr/bin/python3


from brownie import *
import time

root = '888a68797b8c0721b79dd74e30a697a890b8e3ab84f0c5c6c76cec6118402222'
acct = accounts.add(root)

def main():
    # 初始化环境
    print('developer', acct.address)

    testERC20.deploy('FDOT', 'FDOT-Token', 18, {'from': acct})
    testERC20.deploy('FBXH', 'FBXH-Token', 18, {'from': acct})
    testERC20.deploy('FUSDC', 'FUSDC-Token', 8, {'from': acct})
    return 


FDOT = '0xAfb9c2334AF17F362fFcaB0BA3B02286474724e7'
FBXH = '0xfB8409481f2a81222CAe7157F7D1fc343850f9Fc'
FUSDC = '0x39B43b8aE5bEf016AffcF936c915Df09CC114cb7'
