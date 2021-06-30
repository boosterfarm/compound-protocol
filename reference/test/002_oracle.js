const { expect } = require("chai");
const { execute, get } = deployments;

describe("Price Oracle", () => {
  beforeEach(async () => {
    await deployments.fixture();
  });

  it("Should it ok", async () => {
    const signer = await ethers.getNamedSigner('deployer');
    const Oracle = await get('SimplePriceOracle');

    const oracle = await ethers.getContractAt(Oracle.abi, Oracle.address, signer);
    await oracle.setUnderlyingPrice('0xC6f65124FB5f9cF8F4F6aBad03f80B90Dcc28679', ethers.utils.parseUnits('20'));
    await oracle.setUnderlyingPrice('0xB44aAAee673971F7AcAbE31993509067e631b64D', ethers.utils.parseUnits('3'));
  });
});
