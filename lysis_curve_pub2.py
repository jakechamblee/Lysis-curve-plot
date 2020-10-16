def lysis_curve(csv, 
                annotate=False, 
                title=False, 
                group=False, 
                square=750, 
                legend=True, 
                png=False, 
                svg=False):
    '''
    **Given:** CSV, passed as the name of the file in the present directory
    **Returns:** Lysis curve line graph
    *This function always assumes your first column is your time column (x-axis).*
    *Your x-axis data must also be ints not strings if you want the annotations to work properly*
    '''
    import pandas as pd
    import plotly.graph_objs as go

    # Converts csv to Dataframe object
    data = pd.read_csv(csv)
    # Gets column names as list
    columns = list(data.columns)

    # Curated colors to use. Picked for decent contrast
    colors = ['black', 'hotpink', 'cornflowerblue', 'rgb(188, 189, 34)', 'blue',
              'crimson', 'darkgreen', 'lightseagreen', 'navy']

    layout = go.Layout(plot_bgcolor='rgba(0,0,0,0)')
    
    # Creates the plot
    fig = go.Figure(layout=layout)

    if group:
        # This allows the user to color certain (related) line data the same color, but with different line markers
        # User should pass a list of groups as a str, separating each column by a comma as such:
        # ex: [ '1', '2|3', '4|5', '6|7', '8|9' ]
        groups = [x.split('|') for x in group]

        colors = ['rgb(31, 119, 180)',   # blue
                  'rgb(255, 127, 14)',   # orange
                  'rgb(44, 160, 44)',    # green
                  'rgb(214, 39, 40)',    # red
                  'rgb(227, 119, 194)',  # pink
                  'rgb(127, 127, 127)',  # grey
                  'rgb(188, 189, 34)',   # mustard
                  'rgb(23, 190, 207)',
                  'rgb(36, 224, 165)']
        
        markers = ['square',
                   'circle', 
                   'diamond-tall', 
                   'star-square',
                   'hash']

        for i, grp in enumerate(groups):
            group_color = colors[i]
            group_marker = markers[i]
            for k, col in enumerate(grp):
                linemarkers = ['solid', 'dash', 'dot', 'dashdot']
                marker_variant = ['', '-open', '-open-dot']
                fig.add_trace(go.Scatter(
                    x=data[columns[0]],
                    y=data[columns[int(col)]],
                    name=columns[int(col)],
                    connectgaps=True,
                    marker_symbol = group_marker + marker_variant[k],
                    marker_size = 12,
                    marker_opacity = 0.9,
                    marker_line_width=2,
                    #opacity=0.25,
                    line={'color': group_color,
                          'width': 0.6,
                          'dash': linemarkers[k]
                          }
                                        )
                            )
    else:
        # Adds each column to the plot except the first (which is assumed to be the x-axis/time data)
        for i, col in enumerate(columns[1:]):
            fig.add_trace(go.Scatter(
                x=data[columns[0]],
                y=data[col],
                name=col,
                connectgaps=True,
                line=dict(color=colors[i])
            )
            )
    # Graph layout settings
    fig.update_layout(
        yaxis = dict(
        tickmode = 'array',
        tickvals = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        ticktext = [0.01, '', '', '', '', '', '', '', '',0.1, '', '', '', '', '', '', '', '', 1.0, '', '', '', '', '', '', '', '', 10]
                    ),
        # font settings for axes and legend
        font_family="Helvetica",
        font_color="navy",
        font_size=13,
        # font settings for graph title
        title_font_family="Helvetica",
        title_font_color="navy",
                    )
    fig.update_yaxes(title_text='OD550 (log)', 
                     type='log',
                     ticks='inside',
                     showgrid=False,
                     linecolor='black',
                     zeroline=False,
                     mirror=True,
                    #nticks=2,
                    range=[-2,1]
                    )
    fig.update_xaxes(title_text='Time (min)', 
                     showgrid=False, 
                     linecolor='black', 
                     zeroline=False,
                     ticks='inside',
                     tick0=0,
                     dtick=20,
                     mirror=True,
                     # sets range of the xaxis +0.1 b/c the graph border was cutting off markers
                     range=[0, (data[columns[0]].max() +0.1)],
                     constrain="domain", 
                     )
    config = {'displayModeBar': False}

    # Adds annotations to the graph based on the user's input data
    # (i.e. what chemical they used, and when it was added)
    if annotate:
        num_annotations: int = int(
            input('''Enter the number of annotations to add (Ex: if you added DNP to any samples at 10 min and 20 min, enter 2): '''))
        annotation_timepoints = [
            input('Enter your timepoints (Ex: if you added DNP at 40 min and 50 min, enter 40 then 50): ') for i in
            range(num_annotations)]
        annotation_text: str = input('Enter the annotation text (Ex: if DNP added enter DNP): ')

        # creates list of dictionaries for update_layout() detailing where on the x-axis to place the annotations
        annotations = [dict(x=i, y=0.3, text=annotation_text, showarrow=True, arrowhead=4, ax=0, ay=-40) for i in
                       annotation_timepoints]

        fig.update_layout(annotations=annotations)

    if not legend:
        fig.update_layout(showlegend=False)
    
    # Gives user the option to enter a custom graph title. By default, uses the filename
    if title:
        fig.update_layout(
            title={
                'text': f'{title}',
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
    else:
        # Gets csv filename by indexing all but the last 4 characters, the ".csv" part
        csv_name: str = csv[:-4]
        fig.update_layout(
            title={
                'text': f'{csv_name}',
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
    
    csv_name: str = csv[:-4]
    if png:
        # saves the graph as a png in the current directory
        return fig.write_image(f"{csv_name}.png")
    elif svg:
        return fig.write_image(f"{csv_name}.svg", width=square, height=square)
    
    else:
        # shows the graph (for jupyter or a web page)
        return fig.show(config=config)
