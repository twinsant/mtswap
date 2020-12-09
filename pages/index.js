import Head from 'next/head'
import styles from '../styles/Home.module.css'
//import { ChainId, Token, Fetcher } from '@uniswap/sdk'
import { ethers } from 'ethers'
import IUniswapV2Factory from '@uniswap/v2-core/build/IUniswapV2Factory.json'


export default function Home(props) {
  return (
    <div className={styles.container}>
      <Head>
        <title>Hello, Uniswap</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          { props.blocks }
        </h1>
        <p>{ props.name }</p>
        <p>{ props.symbol }</p>
        <p>{ props.totalSupply }</p>
        <h2>Uniswap pairs: { props.allPairsLength }</h2>
      </main>
    </div>
  )
}

export async function getServerSideProps(context) {
  const _network = "homestead"
  const uniswap = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
  const _provider = new ethers.getDefaultProvider(_network, {
    infura: 'project id'
  })
  const uniContract = new ethers.Contract(uniswap, IUniswapV2Factory.abi, _provider)
  const allPairsLength = ethers.BigNumber.from(await uniContract.allPairsLength()).toNumber()

  // const chainId = ChainId.MAINNET
  const tokenAddress = '0x6B175474E89094C44Da98b954EedeAC495271d0F'

  // const DAI = await Fetcher.fetchTokenData(chainId, tokenAddress)

  var network = '未知'
  // if (chainId === 1) {
  //   network = '主网'
  // }else{
  //   network = '测试网络'
  // }

  const provider = new ethers.providers.getDefaultProvider('http://localhost:8545')
  const blocks = await provider.getBlockNumber()

  const address = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
  const ABI = [
    'function name() view returns (string)',
    'function symbol() view returns (string)',
    'function totalSupply() view returns (uint256)',

    'function balanceOf(address) view returns (uint)',

    'function transfer(address to, uint amount)',

    'event Transfer(address indexed from, address indexed to, uint amount)',
  ]
  const contract = new ethers.Contract(address, ABI, provider)
  const name = await contract.name()
  const symbol = await contract.symbol()
  const totalSupply = ethers.BigNumber.from(await contract.totalSupply()).toNumber()

  return {
    props: {
      network,
      blocks,
      name,
      symbol,
      totalSupply,
      allPairsLength,
    }
  }
}
