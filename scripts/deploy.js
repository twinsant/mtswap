// scripts/deploy.js

async function main() {
    // We get the contract to deploy
    const factory = await ethers.getContractFactory("AtomicHabitsToken");
    console.log("Deploying...");
    const contract = await factory.deploy(ethers.BigNumber.from("0"));
    await contract.deployed();
    console.log("Deployed to:", contract.address);
  }
  
  main()
    .then(() => process.exit(0))
    .catch(error => {
      console.error(error);
      process.exit(1);
    });