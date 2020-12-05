import Head from 'next/head'
import styles from '../styles/Home.module.css'
//import { ChainId, Token, Fetcher } from '@uniswap/sdk'
import { ethers } from 'ethers'


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
      </main>
    </div>
  )
}

export async function getServerSideProps(context) {
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

  const address = '0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9'
  const ABI = [
    'function name() view returns (string)',
    'function symbol() view returns (string)',

    'function balanceOf(address) view returns (uint)',

    'function transfer(address to, uint amount)',

    'event Transfer(address indexed from, address indexed to, uint amount)',
  ]
  const contract = new ethers.Contract(address, ABI, provider)
  const name = await contract.name()
  const symbol = await contract.symbol()

  return {
    props: {
      network,
      blocks,
      name,
      symbol
    }
  }
}
