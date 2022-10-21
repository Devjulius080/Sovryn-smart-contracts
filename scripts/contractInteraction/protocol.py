from brownie import *
import json
from scripts.utils import *
import scripts.contractInteraction.config as conf


def isProtocolPaused():
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    print("isProtocolPaused: ", sovryn.isProtocolPaused())


def readLendingFee():
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    lfp = sovryn.lendingFeePercent()
    print(lfp/1e18)
    return lfp


def readLoan(loanId):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    loan = sovryn.getLoan(loanId).dict()
    print('--------------------------------')
    print('loan ID:', loan['loanId'])
    print('principal:', loan['principal'] /1e18)
    print('collateral:', loan['collateral']/1e18)
    print('currentMargin', loan['currentMargin']/1e18)
    print('complete object:')
    print(sovryn.getLoan(loanId).dict())
    print('--------------------------------')
    


def liquidate(protocolAddress, loanId):
    sovryn = Contract.from_abi(
        "sovryn", address=protocolAddress, abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    loan = sovryn.getLoan(loanId).dict()
    print(loan)
    if(loan['maintenanceMargin'] > loan['currentMargin']):
        value = 0
        if(loan['loanToken'] == conf.contracts['WRBTC']):
            value = loan['maxLiquidatable']
        else:
            testToken = Contract.from_abi(
                "TestToken", address=loan['loanToken'], abi=TestToken.abi, owner=conf.acct)
            testToken.approve(sovryn, loan['maxLiquidatable'])
        sovryn.liquidate(loanId, conf.acct,
                         loan['maxLiquidatable'], {'value': value})
    else:
        print("can't liquidate because the loan is healthy")


def rollover(loanId):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    tx = sovryn.rollover(loanId, b'')
    print(tx.info())


def replaceLoanClosings():
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)

    print('replacing loan closings liquidation')
    loanClosingsLiquidationAddress = '0x2d7b3c5B4985A5dA5059AF1466c3FF2fbff4c0A8'
    #loanClosingsLiquidation = conf.acct.deploy(LoanClosingsLiquidation)
    data = sovryn.replaceContract.encode_input(loanClosingsLiquidationAddress)
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)

    print('replacing loan closings rollover')
    loanClosingsRolloverAddress = '0xc424d620bCB1e62D6A3353D6dc6D626b720f1D52'
    #loanClosingsRollover = conf.acct.deploy(LoanClosingsRollover)
    data = sovryn.replaceContract.encode_input(loanClosingsRolloverAddress)
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)

    print('replacing loan closings with')
    loanClosingsWithAddress = '0x88500b472a245a937D07c53B22a107Ce1901d30f'
    #loanClosingsWith = conf.acct.deploy(LoanClosingsWith)
    data = sovryn.replaceContract.encode_input(loanClosingsWithAddress)
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def replaceSwapsExternal():
    swapsExternal = conf.acct.deploy(SwapsExternal)
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.replaceContract.encode_input(swapsExternal.address)
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def replaceLoanOpenings():
    print("replacing loan openings")
    loanOpeningsAddress = '0x78145b66Ee07365CDCf9D79B74100950C641Ba42'
    #loanOpenings = conf.acct.deploy(LoanOpenings)
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.replaceContract.encode_input(loanOpeningsAddress)
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def replaceLoanSettings():
    print("replacing loan settigns")
    loanSettings = conf.acct.deploy(LoanSettings)
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.replaceContract.encode_input(loanSettings.address)
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def replaceSwapsImplSovrynSwap():
    print("replacing swaps")
    swapsAddress = '0x6430a4F15eB72D5066E0405Ed4319F1780665408'
    #swaps = conf.acct.deploy(SwapsImplSovrynSwap)
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.setSwapsImplContract.encode_input(swapsAddress)
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def setLendingFee(fee):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.setLendingFeePercent.encode_input(fee)
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def setTradingFee(fee):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.setTradingFeePercent.encode_input(fee)
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def setBorrowingFee(fee):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.setBorrowingFeePercent.encode_input(fee)
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def setSwapExternalFee(fee):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.setSwapExternalFeePercent.encode_input(fee)
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def setAffiliateFeePercent(fee):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.setAffiliateFeePercent.encode_input(fee)
    print('sovryn.setAffiliateFeePercent for', fee, ' tx:')
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def setAffiliateTradingTokenFeePercent(percentFee):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.setAffiliateTradingTokenFeePercent.encode_input(percentFee)
    print('sovryn.setAffiliateTradingTokenFeePercent for ', percentFee, ' tx:')
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def setMinReferralsToPayout(minReferrals):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.setMinReferralsToPayoutAffiliates.encode_input(minReferrals)
    print('setMinReferralsToPayoutAffiliates set to ', minReferrals, ' tx:')
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def replaceProtocolSettings():
    #print("Deploying ProtocolSettings.")
    settingsAddress = '0x8d15B8Ef9794b68b62DC889F2E5a0F1b0B768268'
    #settings = conf.acct.deploy(ProtocolSettings)

    print("Calling replaceContract.")
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.replaceContract.encode_input(settingsAddress)
    print(data)

    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def replaceLoanSettings():
    #print("Deploying LoanSettings.")
    settingsAddress = '0xab39152B4F3553c28b1b50031D654c83b10BAFc1'
    #settings = conf.acct.deploy(LoanSettings)

    print("Calling replaceContract.")
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.replaceContract.encode_input(settingsAddress)
    print(data)

    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def deployAffiliate():
    # loadConfig() - called from main()
    # -------------------------------- 1. Replace the protocol settings contract ------------------------------
    # replaceProtocolSettings() - called from main()

    # -------------------------------- 2. Deploy the affiliates -----------------------------------------------
    affiliates = conf.acct.deploy(Affiliates)
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.replaceContract.encode_input(affiliates.address)
    print('affiliates deployed. data:')
    print(data)

    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)

    # Set protocolAddress
    data = sovryn.setSovrynProtocolAddress.encode_input(sovryn.address)
    print("Set Protocol Address in protocol settings")
    print(data)

    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)
    # , sovryn.getProtocolAddress()) - not executed yet
    print("protocol address loaded")

    # Set SOVTokenAddress
    # sovToken = Contract.from_abi("SOV", address=conf.contracts["SOV"], abi=SOV.abi, owner=conf.acct)
    # data = sovryn.setSOVTokenAddress.encode_input(sovToken.address)
    data = sovryn.setSOVTokenAddress.encode_input(conf.contracts["SOV"])
    print("Set SOV Token address in protocol settings")
    print(data)

    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)
    # , sovryn.getSovTokenAddress()) - not executed yet
    print("sovToken address loaded")

    # Set LockedSOVAddress
    # lockedSOV = Contract.from_abi("LockedSOV", address=conf.contracts["LockedSOV"], abi=LockedSOV.abi, owner=conf.acct)
    # data = sovryn.setLockedSOVAddress.encode_input(lockedSOV.address)
    data = sovryn.setLockedSOVAddress.encode_input(conf.contracts["LockedSOV"])
    print("Set Locked SOV address in protocol settings")
    print(data)

    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)
    print("lockedSOV address loaded:", lockedSOV.address)

    # Set minReferralsToPayout
    setMinReferralsToPayout(3)

    # Set affiliateTradingTokenFeePercent
    setAffiliateTradingTokenFeePercent(20 * 10**18)

    # Set affiliateFeePercent
    setAffiliateFeePercent(5 * 10**18)

    # ---------------------------- 3. Redeploy modules which implement InterestUser and SwapsUser -----------------------
    # LoanClosingsLiquidation
    # LoanClosingsRollover
    # LoanClosingsWith
    replaceLoanClosings()
    # LoanOpenings
    replaceLoanOpenings()
    # LoanMaintenance
    replaceLoanMaintenance()
    # SwapsExternal
    redeploySwapsExternal()
    # LoanSettings()
    replaceLoanSettings()

    # -------------------------------- 4. Replace Token Logic Standard ----------------------------------------
    replaceLoanTokenLogicOnAllContracts()


def deployAffiliateWithZeroFeesPercent():
    # loadConfig() - called from main()
    # -------------------------------- 1. Replace the protocol settings contract ------------------------------
    # replaceProtocolSettings() - called from main()

    # -------------------------------- 2. Deploy the affiliates -----------------------------------------------

    affiliates = conf.acct.deploy(Affiliates)
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.replaceContract.encode_input(affiliates.address)
    print('affiliates deployed. data:')
    print(data)

    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)

    # Set protocolAddress
    data = sovryn.setSovrynProtocolAddress.encode_input(sovryn.address)
    print("Set Protocol Address in protocol settings")
    print(data)

    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)
    # , sovryn.getProtocolAddress()) - not executed yet
    print("protocol address loaded")

    # Set SOVTokenAddress
    # sovToken = Contract.from_abi("SOV", address=conf.contracts["SOV"], abi=SOV.abi, owner=conf.acct)
    # data = sovryn.setSOVTokenAddress.encode_input(sovToken.address)
    data = sovryn.setSOVTokenAddress.encode_input(conf.contracts["SOV"])
    print("Set SOV Token address in protocol settings")
    print(data)

    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)
    # , sovryn.getSovTokenAddress()) - not executed yet
    print("sovToken address loaded")

    # Set LockedSOVAddress
    # lockedSOV = Contract.from_abi("LockedSOV", address=conf.contracts["LockedSOV"], abi=LockedSOV.abi, owner=conf.acct)
    # data = sovryn.setLockedSOVAddress.encode_input(lockedSOV.address)
    data = sovryn.setLockedSOVAddress.encode_input(conf.contracts["LockedSOV"])
    print("Set Locked SOV address in protocol settings")
    print(data)

    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)
    print("lockedSOV address loaded:", conf.contracts["LockedSOV"])

    # Set minReferralsToPayout
    setMinReferralsToPayout(3)

    # Set affiliateTradingTokenFeePercent
    setAffiliateTradingTokenFeePercent(0)

    # Set affiliateFeePercent
    setAffiliateFeePercent(0)

    # ---------------------------- 3. Redeploy modules which implement InterestUser and SwapsUser -----------------------
    # LoanClosingsLiquidation
    # LoanClosingsRollover
    # LoanClosingsWith
    replaceLoanClosings()
    # LoanOpenings
    replaceLoanOpenings()
    # LoanMaintenance
    replaceLoanMaintenance()
    # SwapsExternal
    redeploySwapsExternal()
    # LoanSettings()
    replaceLoanSettings()

    # -------------------------------- 4. Replace Token Logic Standard ----------------------------------------
    replaceLoanTokenLogicOnAllContracts()


def replaceAffiliates():
    print("replacing Affiliates")
    affiliatesAddress = '0xb756218F36179e26102f7b485aa43031861f5D49'
    #affiliates = conf.acct.deploy(Affiliates)
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.replaceContract.encode_input(affiliatesAddress)
    print(data)

    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def replaceLoanMaintenance():
    print("replacing loan maintenance")
    loanMaintenanceAddress = '0xf5Cb98bEAe74506Fafe4f5824C144bC7907869b0'
    #loanMaintenance = conf.acct.deploy(LoanMaintenance)
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.replaceContract.encode_input(loanMaintenanceAddress)
    print(data)

    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def redeploySwapsExternal():
    print('replacing swaps external')
    swapsExternalAddress = '0x4010bc8A340fB7f9C98053cA2031631c9E575195'
    #swapsExternal = conf.acct.deploy(SwapsExternal)
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.replaceContract.encode_input(swapsExternalAddress)
    print(data)

    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)

# feesControllerAddress = new feeSharingProxy address


def setFeesController(feesControllerAddress):
    print("Set up new fees controller")
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.setFeesController.encode_input(feesControllerAddress)
    print(data)
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def readMaxAffiliateFee():
    abiFile = open('./scripts/contractInteraction/ABIs/SovrynSwapNetwork.json')
    abi = json.load(abiFile)
    swapNetwork = Contract.from_abi(
        "SovrynSwapNetwork", address=conf.contracts['swapNetwork'], abi=abi, owner=conf.acct)
    print(swapNetwork.maxAffiliateFee())


def withdrawFees():
    # Withdraw fees from protocol
    feesController = readFeesController()
    feeSharingProxy = Contract.from_abi(
        "FeeSharingLogic", address=feesController, abi=FeeSharingLogic.abi, owner=conf.acct)
    feeSharingProxy.withdrawFees([
        conf.contracts['USDT'],
        conf.contracts['DoC'],
        conf.contracts['ETHs'],
        conf.contracts['XUSD'],
        conf.contracts['FISH'],
        conf.contracts['BPro'],
        conf.contracts['SOV'],
        conf.contracts['WRBTC'],
    ])

    # Withdraw fees from AMM
    feeSharingProxy.withdrawFeesAMM([
        conf.contracts["ConverterSOV"],
        conf.contracts["ConverterXUSD"],
        conf.contracts["ConverterETHs"],
        conf.contracts["ConverterMOC"],
        conf.contracts["ConverterBNBs"],
        conf.contracts["ConverterFISH"],
        conf.contracts["ConverterRIF"],
        conf.contracts["ConverterMYNT"],
    ])

def setSupportedToken(tokenAddress):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.setSupportedTokens.encode_input([tokenAddress], [True])
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def deployConversionFeeSharingToWRBTC():
    # For first time deployment of Upgradable FeeSharingProxy (v2), need to call deployFeeSharingProxy first to deploy the proxy
    # After deployFeeSharingProxyCalled, need to store the address to the testnet_contracts.json with variable name = FeeSharingProxy2

    print("Redeploy fee sharing logic")
    # Redeploy feeSharingLogic
    feeSharing = conf.acct.deploy(FeeSharingLogic)
    print("Fee sharing logic redeployed at: ", feeSharing.address)

    print("Set implementation for FeeSharingProxy")
    feeSharingProxy = Contract.from_abi(
        "FeeSharingProxy", address=conf.contracts['FeeSharingProxy'], abi=FeeSharingProxy.abi, owner=conf.acct)
    data = feeSharingProxy.setImplementation.encode_input(feeSharing.address)
    sendWithMultisig(conf.contracts['multisig'],
                     feeSharingProxy.address, data, conf.acct)

    # Redeploy protocol settings
    replaceProtocolSettings()

    # Redeploy swaps external
    redeploySwapsExternal()

    # Set Fees Controller
    setFeesController(feeSharingProxy.address)


def deployFeeSharingProxy():
    print("Deploy fee sharing proxy")
    feeSharingProxy = conf.acct.deploy(
        FeeSharingProxy, conf.contracts['sovrynProtocol'], conf.contracts['Staking'])
    print(feeSharingProxy.address)
    print('Proxy owner: ', feeSharingProxy.getProxyOwner())
    print('FeeSharingProxy ownership: ', feeSharingProxy.owner())
    feeSharingProxy.setProxyOwner(conf.contracts['multisig'])
    feeSharingProxy.transferOwnership(conf.contracts['multisig'])
    print('New proxy owner: ', feeSharingProxy.getProxyOwner())
    print('New FeeSharingProxy ownership: ', feeSharingProxy.owner())


def setSupportedTokens(tokenAddresses, supported):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.setSupportedTokens.encode_input(tokenAddresses, supported)
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def tokenIsSupported(tokenAddress):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.supportedTokens(tokenAddress)
    print(data)


def deployTradingRebatesUsingLockedSOV():
    # loadConfig()

    sovryn = Contract.from_abi(
        "sovryn", address=contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=acct)

    # ----------------------------- 1. Replace Protocol Settings ------------------------------
    # replaceProtocolSettings()

    # ----------------------------- 2. Set protocol token address using SOV address ------------------------------
    # sovToken = Contract.from_abi("SOV", address=contracts["SOV"], abi=SOV.abi, owner=acct)
    # data = sovryn.setProtocolTokenAddress.encode_input(sovToken.address)
    # print("Set Protocol Token address in protocol settings")
    # print(data)

    # multisig = Contract.from_abi("MultiSig", address=contracts['multisig'], abi=MultiSigWallet.abi, owner=acct)
    # tx = multisig.submitTransaction(sovryn.address,0,data)
    # txId = tx.events["Submission"]["transactionId"]
    # print(txId)
    # print("protocol token address loaded:", sovryn.sovTokenAddress())

    # ----------------------------- 3. Set LockedSOV address -------------------------------------------
    # lockedSOV = Contract.from_abi("LockedSOV", address=contracts["LockedSOV"], abi=LockedSOV.abi, owner=acct)
    # data = sovryn.setLockedSOVAddress.encode_input(lockedSOV.address)
    # print("Set Locked SOV address in protocol settings")
    # print(data)

    # multisig = Contract.from_abi("MultiSig", address=contracts['multisig'], abi=MultiSigWallet.abi, owner=acct)
    # tx = multisig.submitTransaction(sovryn.address,0,data)
    # txId = tx.events["Submission"]["transactionId"]
    # print(txId)
    # print("lockedSOV address loaded:", sovryn.sovTokenAddress())

    # ----------------------------- 4. Set default feeRebatePercent -------------------------------------------
    setDefaultRebatesPercentage(10 * 10**18)

    # TODO
    # setSpecialRebates("sourceTokenAddress", "destTokenAddress", 10 * 10**18)

    # ---------------------------- 5. Redeploy modules which implement InterestUser and SwapsUser -----------------------
    # LoanClosingsLiquidation
    # LoanClosingsRollover
    # LoanClosingsWith
    replaceLoanClosings()
    # LoanOpenings
    replaceLoanOpenings()
    # LoanMaintenance
    replaceLoanMaintenance()
    # SwapsExternal
    redeploySwapsExternal()
    # LoanSettings
    replaceLoanSettings()

    # ---------------------------- 5. Set the basis point of SOV Rewards (Ratio between vested & the liquid one for the LockedSOV) -----------------------
    # 90% liquid, 10% vested
    setTradingRebateRewardsBasisPoint(9000)


def setDefaultRebatesPercentage(rebatePercent):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.setRebatePercent.encode_input(rebatePercent)
    multisig = Contract.from_abi(
        "MultiSig", address=conf.contracts['multisig'], abi=MultiSigWallet.abi, owner=conf.acct)
    tx = multisig.submitTransaction(sovryn.address, 0, data)
    txId = tx.events["Submission"]["transactionId"]
    print(txId)


def setTradingRebateRewardsBasisPoint(basisPoint):
    # Max basis point is 9999
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.setTradingRebateRewardsBasisPoint.encode_input(basisPoint)
    multisig = Contract.from_abi(
        "MultiSig", address=conf.contracts['multisig'], abi=MultiSigWallet.abi, owner=conf.acct)
    tx = multisig.submitTransaction(sovryn.address, 0, data)
    txId = tx.events["Submission"]["transactionId"]
    print(txId)

def pauseProtocolModules():
    print("Pause Protocol Modules")
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.togglePaused.encode_input(True)
    print(data)

    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def unpauseProtocolModules():
    print("Unpause Protocol Modules")
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.togglePaused.encode_input(False)
    print(data)

    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)


def minInitialMargin(loanParamsId):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    print(sovryn.minInitialMargin(loanParamsId))

def addWhitelistConverterFeeSharingProxy(converterAddress):
    feeSharingProxy = Contract.from_abi("FeeSharingLogic", address=conf.contracts['FeeSharingProxy'], abi=FeeSharingLogic.abi, owner=conf.acct)
    data = feeSharingProxy.addWhitelistedConverterAddress.encode_input(converterAddress)
    print(data)

    sendWithMultisig(conf.contracts['multisig'], feeSharingProxy.address, data, conf.acct)

def removeWhitelistConverterFeeSharingProxy(converterAddress):
    feeSharingProxy = Contract.from_abi("FeeSharingLogic", address=conf.contracts['FeeSharingProxy'], abi=FeeSharingLogic.abi, owner=conf.acct)
    data = feeSharingProxy.removeWhitelistedConverterAddress.encode_input(converterAddress)

    print(data)
    sendWithMultisig(conf.contracts['multisig'], feeSharingProxy.address, data, conf.acct)

def readRolloverReward():
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    print(sovryn.rolloverBaseReward())

def withdrawWRBTCFromFeeSharingProxyToProtocol(amount):
    receiver = conf.contracts['sovrynProtocol']
    feeSharingProxy = Contract.from_abi("FeeSharingLogic", address=conf.contracts['FeeSharingProxy'], abi=FeeSharingLogic.abi, owner=conf.acct)
    wrbtc = Contract.from_abi("WRBTC", address=conf.contracts['WRBTC'], abi=ERC20.abi, owner=conf.acct)
    print("=============================================================")
    print('withdrawWRBTCFromFeeSharingProxyToProtocol')
    print("FeeSharingProxy WRBTC balance:  ", wrbtc.balanceOf(conf.contracts['FeeSharingProxy']))
    print("receiver:                       ", receiver)
    print("amount to withdraw:             ", amount)
    print("=============================================================")
    withdrawWRBTCFromFeeSharingProxy(receiver, amount)

def withdrawWRBTCFromFeeSharingProxy(receiver, amount):
    feeSharingProxy = Contract.from_abi("FeeSharingLogic", address=conf.contracts['FeeSharingProxy'], abi=FeeSharingLogic.abi, owner=conf.acct)
    data = feeSharingProxy.withdrawWRBTC.encode_input(receiver, amount)
    print(data)
    sendWithMultisig(conf.contracts['multisig'], feeSharingProxy.address, data, conf.acct)

def setRolloverFlexFeePercent(rolloverFlexFeePercentage):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.setRolloverFlexFeePercent.encode_input(rolloverFlexFeePercentage)
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)

def setRolloverBaseReward(baseReward):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.setRolloverBaseReward.encode_input(baseReward)
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)

def depositCollateral(loanId,depositAmount, tokenAddress):
    token = Contract.from_abi("TestToken", address = tokenAddress, abi = TestToken.abi, owner = conf.acct)
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    if(token.allowance(conf.acct, sovryn.address) < depositAmount):
        token.approve(sovryn.address, depositAmount)
    sovryn.depositCollateral(loanId,depositAmount)

def setDefaultPathConversion(sourceTokenAddress, destTokenAddress, defaultPath):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.setDefaultPathConversion.encode_input(defaultPath)
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)

def removeDefaultPathConversion(sourceTokenAddress, destTokenAddress):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.removeDefaultPathConversion.encode_input(sourceTokenAddress, destTokenAddress)
    sendWithMultisig(conf.contracts['multisig'],
                     sovryn.address, data, conf.acct)

def readDefaultPathConversion(sourceTokenAddress, destTokenAddress):
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    defaultPathConversion = sovryn.getDefaultPathConversion(sourceTokenAddress, destTokenAddress)
    print(defaultPathConversion)
    return defaultPathConversion

# Transferring Ownership to GOV
def transferProtocolOwnershipToGovernance():
    print("Transferring sovryn protocol ownserhip to: ", conf.contracts['TimelockOwner'])
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    data = sovryn.transferOwnership.encode_input(conf.contracts['TimelockOwner'])
    sendWithMultisig(conf.contracts['multisig'], sovryn.address, data, conf.acct)

def readFeesController():
    sovryn = Contract.from_abi(
        "sovryn", address=conf.contracts['sovrynProtocol'], abi=interface.ISovrynBrownie.abi, owner=conf.acct)
    feesController = sovryn.feesController()
    print(feesController)
    return feesController