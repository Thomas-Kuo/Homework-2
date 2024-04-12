# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Solution
- Swap 5 tokenB to 5.655321988655322 tokenA
- Swap 5.655321988655322 tokenA to 2.37213893638309 tokenC
- Swap 2.37213893638309 tokenC to 1.5301371369636172 tokenE
- Swap 1.5301371369636172 tokenE to 3.450741448619709 tokenD
- Swap 3.450741448619709 tokenD to 6.68452557957259 tokenC
- Swap 6.68452557957259 tokenC to 22.497221806974142 tokenB
- path: tokenB->tokenA->tokenC->tokenE->tokenD->tokenC->tokenB, tokenB balance=22.497221806974142

![image](https://github.com/Thomas-Kuo/Homework-2/blob/main/hw2/image/profitable%20path.png)

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Solution

Slippage in AMM (Automated Market Maker) refers to the difference between the expected price of a trade and the price at which the trade is actually executed. This discrepancy can occur due to changes in the pool's state between the time a transaction is submitted and when it is executed, particularly in volatile markets or during large trades.

Uniswap V2 addresses slippage by allowing users to specify a minimum amount of output tokens (`amountOutMin`) they are willing to accept for a given input amount. This mechanism ensures that the trade will revert if the price moves unfavorably beyond the user's tolerance for slippage.

For example, consider the function `swapExactTokensForTokens` in Uniswap V2:

```solidity
function swapExactTokensForTokens(
uint amountIn,
uint amountOutMin,
address[] calldata path,
address to,
uint deadline
) external returns (uint[] memory amounts);
```

- `amountIn`: The amount of input tokens that the user is trading.
- `amountOutMin`: The minimum amount of output tokens that the user is willing to accept.
- `path`: An array of token addresses which the trade will go through.
- `to`: The address that will receive the output tokens.
- `deadline`: A timestamp by which the trade must be completed, to ensure the trade is not executed too far in the future.

Here, `amountOutMin` plays a crucial role. If the actual amount of output tokens that can be received is less than `amountOutMin` due to slippage, the transaction will fail. This parameter allows users to control their maximum acceptable slippage.

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> Solution

In the UniswapV2Pair contract, the `mint` function is responsible for adding liquidity to the pool and minting the pool's liquidity tokens to the provider. A distinctive feature of this function is that during the initial liquidity provision, a minimum liquidity amount, defined as `MINIMUM_LIQUIDITY`, is subtracted and permanently locked in the pool. The rationale behind this design is multifaceted:

1. **Preventing Division by Zero**: In the AMM model used by Uniswap, prices are determined by the ratio of the two assets in the liquidity pool. If the pool were to be completely drained, it could potentially lead to division by zero errors when calculating prices. By ensuring that a small amount of liquidity is always present, the contract guards against such scenarios.

2. **Token Value**: By locking away a small amount of liquidity tokens (specifically 1e-3 liquidity tokens), Uniswap ensures that the pool cannot be completely drained. This gives the liquidity tokens a base value and prevents certain types of manipulation or attacks where a pool could be drained entirely.

3. **Ownership Representation**: The minted liquidity tokens represent a proportional share of the pool's total liquidity. By locking away a small initial share, Uniswap ensures that the first liquidity provider doesn't own 100% of the pool by only providing an infinitesimally small amount of liquidity.

Here's a simplified overview of the `mint` function's logic concerning the initial liquidity provision:

```solidity
function mint(address to) external returns (uint liquidity) {
    (uint112 _reserve0, uint112 _reserve1,) = getReserves(); // fetches the reserves
    uint balance0 = IERC20(token0).balanceOf(address(this));
    uint balance1 = IERC20(token1).balanceOf(address(this));
    uint amount0 = balance0 - _reserve0;
    uint amount1 = balance1 - _reserve1;

    if (totalSupply == 0) {
        // During the first minting, subtract the MINIMUM_LIQUIDITY
        liquidity = Math.sqrt(amount0 * amount1) - MINIMUM_LIQUIDITY;
        _mint(address(0), MINIMUM_LIQUIDITY); // lock the minimum liquidity forever
    } else {
        liquidity = Math.min(amount0 * totalSupply / _reserve0, amount1 * totalSupply / _reserve1);
    }

    _mint(to, liquidity);
    update(balance0, balance1, _reserve0, _reserve1);
    return liquidity;
}
```

The `MINIMUM_LIQUIDITY` subtraction acts as a safeguard against potential issues and ensures the integrity and robustness of the liquidity provision process in Uniswap V2.

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> Solution

In the UniswapV2Pair contract, the `mint` function is used to add liquidity to the pool. For subsequent liquidity provisions (after the initial one), the amount of liquidity tokens minted is determined by a specific formula, which is intended to maintain the ratio of the liquidity provider's share relative to the total liquidity in the pool.

Here's the formula used when minting liquidity tokens during subsequent deposits:

$$ \text{liquidity} = \min\left(\frac{\text{amount0} \times \text{totalSupply}}{\text{reserve0}}, \frac{\text{amount1} \times \text{totalSupply}}{\text{reserve1}}\right) $$

Where:
- `amount0` and `amount1` are the amounts of the two tokens being deposited.
- `reserve0` and `reserve1` are the current reserves (liquidity) of the two tokens in the pool.
- `totalSupply` is the total supply of the liquidity tokens.

The intention behind this formula is to ensure that the share of liquidity tokens minted for the provider is proportional to the amount of liquidity they are adding relative to the existing liquidity in the pool. This mechanism serves several purposes:

1. **Fair Distribution**: It ensures that the liquidity tokens a provider receives are proportional to their contribution to the pool's liquidity. This fair distribution mechanism prevents dilution or unfair advantages, ensuring that earlier or later providers get a fair share of the pool's fees based on their contributed liquidity.

2. **Value Preservation**: By tying the minted liquidity tokens to the relative share of liquidity added, this approach ensures that the value of existing liquidity tokens isn't diluted by new additions. Each liquidity token represents a fractional ownership of the pool's total assets, and this relationship is preserved through the formula.

3. **Incentive Alignment**: This formula aligns the incentives of liquidity providers with the health of the pool. Providers are encouraged to add liquidity in a balanced manner, reflecting the current price ratio in the pool, which in turn helps maintain the overall stability and efficiency of the market mechanism.

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> Solution

A sandwich attack is a type of front-running attack specifically targeting decentralized finance (DeFi) platforms and automated market makers (AMMs) like Uniswap. In a sandwich attack, a malicious actor capitalizes on a pending transaction in the mempool that they spot and expects to significantly impact the price of a token pair.

Here’s how a sandwich attack typically unfolds:

1. **Detection**: The attacker detects a large trade initiated by a user that is yet to be processed but is visible in the mempool. This trade is significant enough to shift the market price once executed.

2. **Front-Running**: The attacker executes a trade (the "front" trade) just before the user’s trade, buying the same token that the user intends to buy but at the current, lower price. This action increases the price of the token due to added demand.

3. **Back-Running**: After the user’s trade is executed, which further increases the price due to significant demand, the attacker executes a second trade (the "back" trade). In this trade, the attacker sells the token at an elevated price, capitalizing on the price movement caused by the user’s trade.

Impact on the User:
- **Increased Price Impact**: The user’s trade is executed at a less favorable rate because the attacker’s front trade has already moved the price.
- **Value Extraction**: The user indirectly loses value to the attacker, who profits from the price discrepancies before and after the user’s trade.
- **Market Efficiency**: While such attacks exploit arbitrage opportunities, they also highlight inefficiencies and potential vulnerabilities in AMM designs, leading to a broader discussion about improving these systems.

## Bonus
Please provide the most profitable path among all possible swap paths and the corresponding Python script, along with its profit. Only the accurate answer will be accepted

> Solution
- path: tokenB->tokenA->tokenC->tokenE->tokenD->tokenC->tokenB, tokenB balance=22.497221806974142
