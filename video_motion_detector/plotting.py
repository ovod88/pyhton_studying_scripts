# from detector import df# TO DO df dynamically with camera launch
import pandas

from bokeh.plotting import figure, output_file, show, reset_output
from bokeh.models import HoverTool, ColumnDataSource

df = pandas.read_csv("Times.csv", parse_dates=['Start', 'End'])#Using correct Times file from detector.py file withou camera launch
df['Start_string'] = df['Start'].dt.strftime('%Y-%m-%d %H:%M:%S')
df['End_string'] = df['End'].dt.strftime('%Y-%m-%d %H:%M:%S')

cds = ColumnDataSource(df)
# print(df[['Start', 'End']])
# print(df['Start'][0])
p = figure(x_axis_type='datetime', height=100, width=500,
			sizing_mode='scale_width', title='Motion graph')
p.quad(left='Start', right='End', bottom=0, top=1, color='green', source=cds)
p.yaxis.minor_tick_line_color=None
p.ygrid[0].ticker.desired_num_ticks = 1

hover = HoverTool(tooltips=[('Start ', '@Start_string'), ('End ', '@End_string')])
p.add_tools(hover)

reset_output()
output_file("Motion_detection.html")
show(p)