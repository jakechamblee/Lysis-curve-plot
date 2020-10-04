def lysis_curve(csv, annotate=False, png=False, title=False, group=False):
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
    colors = ['black', 'pink', 'cornflowerblue', 'grey', 'blue', 'crimson', 'darkgreen', 'lightseagreen', 'navy']

    # Creates the plot
    fig = go.Figure()

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
                  'rgb(127, 127, 127)',
                  'rgb(188, 189, 34)',
                  'rgb(23, 190, 207)']

        for i, grp in enumerate(groups):
            group_color = colors[i]
            for k, col in enumerate(grp):
                markers = ['solid', 'dash', 'dashdot', 'dot']
                fig.add_trace(go.Scatter(
                    x=data[columns[0]],
                    y=data[columns[int(col)]],
                    name=columns[int(col)],
                    connectgaps=True,
                    line={'color': group_color,
                          'width': 3,
                          'dash': markers[k]
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
    fig.update_yaxes(title_text='OD550 (log)', type='log', nticks=2, ticks='inside', tickmode='linear', showgrid=False)
    fig.update_xaxes(title_text='Time (min)')

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

    if png:
        csv_name: str = csv[:-4]
        # saves the graph as a png in the current directory
        return fig.write_image(f"{csv_name}.png")
    else:
        # shows the graph (for jupyter or a web page)
        return fig.show()
