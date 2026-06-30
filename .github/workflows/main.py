from data import load_data
from factors import add_factors
from ic_rolling import rolling_ic, mean_ic, ic_stability
from portfolio_mvo import markowitz
from backtest import backtest
from report import send


def main():

    df = load_data()
    df = add_factors(df)

    # =====================
    # 1. 构建 score（因子合成）
    # =====================
    df["score"] = (
        df["涨跌幅"].rank(pct=True) * 0.4 +
        df["换手率"].rank(pct=True) * 0.3 +
        df["成交额"].rank(pct=True) * 0.2 +
        (-df["振幅"].rank(pct=True)) * 0.1
    )

    # =====================
    # 2. 滚动IC分析
    # =====================
    ic_mom = rolling_ic(df, "涨跌幅")

    ic_mean = mean_ic(ic_mom)
    ic_std = ic_stability(ic_mom)

    # =====================
    # 3. Markowitz优化
    # =====================
    df = markowitz(df)

    # =====================
    # 4. 回测组合
    # =====================
    stats = backtest(df)

    # =====================
    # 5. 输出报告
    # =====================
    msg = "📊 滚动IC + Markowitz量化系统\n\n"

    msg += f"📈 IC均值: {ic_mean:.3f}\n"
    msg += f"📉 IC稳定性(Std): {ic_std:.3f}\n\n"

    msg += "📊 组合表现:\n"
    msg += f"收益: {stats['收益']}%\n"
    msg += f"波动: {stats['波动']}\n"
    msg += f"夏普: {stats['夏普']}\n\n"

    msg += "📌 Top权重股票:\n"

    top = df.sort_values("weight", ascending=False).head(10)

    for _, r in top.iterrows():
        msg += f"{r['代码']} {r['名称']} w={r['weight']:.3f}\n"

    send(msg)


if __name__ == "__main__":
    main()
