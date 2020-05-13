import plotly.express as px
import pandas as pd
df = px.data.tips()
import plotly.io as pio

#pio.renderers.default = 'svg'

# file structure:
# instance        Dim      LOCAL     1 TASK    8 TASKS

#conda install -c plotly plotly=4.7.1
#conda install -c plotly plotly-orca

print(df.columns)
data = pd.read_csv('awsecs.csv')
print(data.dtypes)

fig = px.box(data, x = "Dimension", y = "Ratio", color = "Environment",  points='all' )

#fig = px.box(data, Dim="local")
#fig.show()
fig.write_image("fig1.pdf", width = 1080, height = 700 )