// scripts/deploy.js

async function main() {
    // We get the contract to deploy
    const factory = await ethers.getContractFactory("AtomicHabitToken");
    console.log("Deploying...");
    const contract = await factory.deploy(ethers.BigNumber.from("20000"));
    await contract.deployed();
    console.log("Deployed to:", contract.address);
  }
  
  main()
    .then(() => process.exit(0))
    .catch(error => {
      console.error(error);
      process.exit(1);
    });