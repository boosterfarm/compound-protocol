const { expect } = require("chai");
const { execute, get } = deployments;

describe("Comptroller", () => {
  beforeEach(async () => {
    await deployments.fixture();
  });

  it("Should basic information ok", async () => {
    const { deployer } = await getNamedAccounts();

    const Unitroller   = await get('Unitroller');
    const Comptroller  = await get('Comptroller');

    const unitroller   = await ethers.getContractAt(Comptroller.abi, Unitroller.address);
    const comptroller  = await ethers.getContractAt(Comptroller.abi, Comptroller.address);

    const impl = await unitroller.comptrollerImplementation();
    expect(impl).to.equal(Comptroller.address);

    const admin1 = await unitroller.admin();
    const admin2 = await comptroller.admin();
    expect(admin1).to.equal(admin2);
    expect(admin1).to.equal(deployer);
  });

  it("Should it set COMP address ok", async () => {
    const { deployer } = await getNamedAccounts();

    const Comptroller  = await get('Comptroller');
    const Unitroller   = await get('Unitroller');

    const signer     = await ethers.getNamedSigner('deployer');
    const unitroller = await ethers.getContractAt(Comptroller.abi, Unitroller.address, signer);

    let comp = await unitroller.compAddress();
    expect(comp).to.equal(ethers.constants.AddressZero);

    await unitroller._setCompAddress(deployer);
    comp = await unitroller.compAddress();
    expect(comp).to.equal(deployer);
  })
});
