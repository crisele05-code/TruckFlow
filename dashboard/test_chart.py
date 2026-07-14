from repository import get_top_clienti
from charts import plot_top_clienti

df = get_top_clienti()

fig = plot_top_clienti(df)

fig.show()