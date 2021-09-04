import pymc3 as pm


def plot_traces(traces, model, retain=0):
    """
    Convenience function:
    Plot traces with overlaid means and values
    """
    with model:
        ax = pm.traceplot(
            traces[-retain:],
            lines=tuple([(k, {}, v["mean"])
                         for k, v in pm.summary(traces[-retain:]).iterrows()]),
        )

        for i, mn in enumerate(pm.summary(traces[-retain:])["mean"]):
            ax[i, 0].annotate(
                f"{mn:.2f}",
                xy=(mn, 0),
                xycoords="data",
                xytext=(5, 10),
                textcoords="offset points",
                rotation=90,
                va="bottom",
                fontsize="large",
                color="#AA0022",
            )
