import numpy as np
import pandas as pd

def markowitz(df):
    """
    简化Markowitz：均值-方差优化
    """

    returns = df["涨跌幅"].values

    # 协方差矩阵（简化：单日横截面）
    cov = np.cov(returns)

    # 防止除0
    inv_cov = 1 / (np.var(returns) + 1e-6)

    # 用 score 当收益预期
    expected = df["score"].values

    weights = expected * inv_cov

    weights = weights / np.sum(weights)

    df = df.copy()
    df["weight"] = weights

    return df
