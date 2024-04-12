# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Solution
Swap 5 tokenB to 5.655321988655322 tokenA
Swap 5.655321988655322 tokenA to 2.37213893638309 tokenC
Swap 2.37213893638309 tokenC to 1.5301371369636172 tokenE
Swap 1.5301371369636172 tokenE to 3.450741448619709 tokenD
Swap 3.450741448619709 tokenD to 6.68452557957259 tokenC
Swap 6.68452557957259 tokenC to 22.497221806974142 tokenB
path: tokenB->tokenA->tokenC->tokenE->tokenD->tokenC->tokenB, tokenB balance=22.497221806974142

![image](https://github.com/Thomas-Kuo/Homework-2/blob/main/hw2/image/profitable%20path.png)

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Solution

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> Solution

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> Solution

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> Solution

