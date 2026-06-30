import pandas as pd

def rolling_ic(df, factor, window=5):
    """
    简化版滚动IC
    """

    ic_list = []

    for i in range(window, len(df)):
        sub = df.iloc[i-window:i]

        ic = sub[factor].corr(sub["涨跌幅"], method="spearman")
        ic_list.append(ic)

    return pd.Series(ic_list)


def mean_ic(ic_series):
    return ic_series.mean()


def ic_stability(ic_series):
    return ic_series.std()
