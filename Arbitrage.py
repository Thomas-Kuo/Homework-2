# liquidity = {
#     ("tokenA", "tokenB"): (17, 10), A 5.67 1st
#     ("tokenA", "tokenC"): (11, 7),
#     ("tokenA", "tokenD"): (15, 9),
#     ("tokenA", "tokenE"): (21, 5), E 1.07 2nd
#     ("tokenB", "tokenC"): (36, 4), B 20 5th
#     ("tokenB", "tokenD"): (13, 6),
#     ("tokenB", "tokenE"): (25, 3),
#     ("tokenC", "tokenD"): (30, 12), C 5 4th
#     ("tokenC", "tokenE"): (10, 8),
#     ("tokenD", "tokenE"): (60, 25), D 2.3 3rd
# }

# liquidity = {
#     ("tokenA", "tokenB"): (17, 10), A 5.66
#     ("tokenA", "tokenC"): (11, 7), C 2.37
#     ("tokenA", "tokenD"): (15, 9),
#     ("tokenA", "tokenE"): (21, 5),
#     ("tokenB", "tokenC"): (36, 4), 22.51
#     ("tokenB", "tokenD"): (13, 6),
#     ("tokenB", "tokenE"): (25, 3),
#     ("tokenC", "tokenD"): (30, 12), C 6.7
#     ("tokenC", "tokenE"): (10, 8), E 1.53
#     ("tokenD", "tokenE"): (60, 25), D 3.46
# }

liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

def get_swap_amount(x_amount, x_reserves, y_reserves):
    # 计算扣除交易手续费后用于交易的x代币数量
    x_amount_with_fee = x_amount * 0.997
    
    # 使用恒定乘积公式计算y代币的输出数量
    # 注意这里我们先计算新的x储备量，然后使用这个新的储备量来计算y的减少量
    new_x_reserves = x_reserves + x_amount_with_fee
    y_amount = y_reserves - (y_reserves * x_reserves) / new_x_reserves

    return y_amount


def find_profitable_path(current_token, current_amount, path, visited, transaction_details):
    if current_token == 'tokenB' and len(path) > 1 and current_amount > 22.497:
        for detail in transaction_details:
            print(f"Swap {detail['amountIn']} {detail['from']} to {detail['amountOut']} {detail['to']}")
        path_output = "->".join(path)
        print(f"path: {path_output}, tokenB balance={current_amount}")
        return (True, path, transaction_details, current_amount)
    
    for (token1, token2), (reserve1, reserve2) in liquidity.items():
        if token1 == current_token and (token1, token2) not in visited:
            next_amount = get_swap_amount(current_amount, reserve1, reserve2)
            result = find_profitable_path(token2, next_amount, path + [token2], visited + [(token1, token2)], transaction_details + [{'from': token1, 'to': token2, 'amountIn': current_amount, 'amountOut': next_amount}])
            if result[0]:
                return result
        elif token2 == current_token and (token2, token1) not in visited:
            next_amount = get_swap_amount(current_amount, reserve2, reserve1)
            result = find_profitable_path(token1, next_amount, path + [token1], visited + [(token2, token1)], transaction_details + [{'from': token2, 'to': token1, 'amountIn': current_amount, 'amountOut': next_amount}])
            if result[0]:
                return result
    return (False, [], [], 0)

# 使用初始tokenB数量为5开始搜索
result = find_profitable_path('tokenB', 5, ['tokenB'], [], [])

# 检查搜索结果，如果没有找到路径，输出失败消息
if not result[0]:
    print("Failed to find a profitable path where tokenB balance exceeds 22.498.")



