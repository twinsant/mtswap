// scripts/index.js
async function main() {
  // Our code will go here
  // Retrieve accounts from the local node
  const accounts = await ethers.provider.listAccounts();
  console.log(accounts);

  // Set up an ethers contract, representing our deployed Box instance
  const address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
  const factory = await ethers.getContractFactory("AtomicHabitsToken");
  const token = await factory.attach(address);

  const name = await token.name();
  console.log("Token name is", name);
}
  
  main()
    .then(() => process.exit(0))
    .catch(error => {
      console.error(error);
      process.exit(1);
    });