from flask import Flask, render_template
import plotly.graph_objs as go
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import pandas as pd
import plotly.express as px
import plotly.offline as pyo
import pickle


# Create a Flask application
app = Flask(__name__)

def test():
    # Load data
    df = pd.read_csv('../back_end/static_data_with_emebddings.csv')
    
    matrix = np.array(df.ada_embedding.apply(eval).to_list() )  
   
    # tsne = TSNE(n_components=3, perplexity=15, random_state=42, init='random', learning_rate=200, )
    # vis_dims = tsne.fit_transform(matrix)
    # apply PCA to reduce the dimensionality of the embedding vectors

    # pca = PCA(n_components=3)
    # vis_dims = pca.fit_transform(matrix)


    # with open('vis_dims.pkl', 'wb') as f:
    #     pickle.dump(vis_dims, f)

    with open('vis_dims.pkl', 'rb') as f:
        vis_dims = pickle.load(f)
    

    fig = px.scatter_3d(vis_dims, x=0, y=1, z=2, opacity=0, color=df["subject_descr"])
    
    
    
    # fig.update_traces(customdata=df["subject_descr"].values[:, np.newaxis])
    # Create the 3D plot using Plotly
    # fig = px.scatter_3d(vis_dims, x=0, y=1, z=2, opacity=0, color = df["subject_descr"])

    fig.update_traces(hovertemplate='<b>Subject:</b> %{customdata[0]}<extra></extra>', customdata=df["subject_descr"].values[:, np.newaxis])
    
    
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False,zaxis_visible=False )

    # make the background and space around points transparent
    fig.update_layout(scene=dict(bgcolor='rgba(0,0,0,0)'))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    # remove gridlines
    fig.update_layout(scene=dict(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), zaxis=dict(showgrid=False)))   
    # make the background transparent
    # fig.update_layout(scene=dict(bgcolor='rgba(0,0,0,0)'))
    fig.update_layout(scene=dict(bgcolor='rgba(0,0,0,0)'))
    return render_template('plot.html', plot=fig.to_html(full_html=False))

    # Show the plot
    # fig.show()

    # pyo.plot(fig, filename='my_plot.html', output_type='div', include_plotlyjs=False, auto_open=False, config={'displayModeBar': False})




# test()

# Define a route for the webpage
@app.route('/')
def index():
    
        # Load data
    df = pd.read_csv('../back_end/static_data_with_emebddings.csv')
    
    matrix = np.array(df.ada_embedding.apply(eval).to_list() )  
   
    # tsne = TSNE(n_components=3, perplexity=15, random_state=42, init='random', learning_rate=200, )
    # vis_dims = tsne.fit_transform(matrix)
    # apply PCA to reduce the dimensionality of the embedding vectors

    # pca = PCA(n_components=3)
    # vis_dims = pca.fit_transform(matrix)


    # with open('vis_dims.pkl', 'wb') as f:
    #     pickle.dump(vis_dims, f)

    with open('vis_dims.pkl', 'rb') as f:
        vis_dims = pickle.load(f)
    

    fig = px.scatter_3d(vis_dims, x=0, y=1, z=2, opacity=0, color=df["subject_descr"])
    
    
    
    # fig.update_traces(customdata=df["subject_descr"].values[:, np.newaxis])
    # Create the 3D plot using Plotly
    # fig = px.scatter_3d(vis_dims, x=0, y=1, z=2, opacity=0, color = df["subject_descr"])

    fig.update_traces(hovertemplate='<b>Subject:</b> %{customdata[0]}<extra></extra>', customdata=df["subject_descr"].values[:, np.newaxis])
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False,zaxis_visible=False )

    # make the background and space around points transparent
    fig.update_layout(scene=dict(bgcolor='rgba(0,0,0,0)'))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    # remove gridlines
    fig.update_layout(scene=dict(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), zaxis=dict(showgrid=False)))   
    # make the background transparent
    # fig.update_layout(scene=dict(bgcolor='rgba(0,0,0,0)'))
    fig.update_layout(scene=dict(bgcolor='rgba(0,0,0,0)'))
    return render_template('plot.html', plot=fig.to_html(full_html=False))

    
    # Generate some random data
    # Generate some random data
    # Generate some random data
    # x, y, z = np.random.multivariate_normal([0,0,0], np.eye(3), 500).transpose()

    # # Create a 3D scatter plot
    # trace = go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=5, color=z, colorscale='Viridis', opacity=0.8))

    # # Set the background color and font color
    # bgcolor = '#1f1f1f'
    # fontcolor = '#FFFFFF'

    # # Create a layout for the plot
    # layout = go.Layout(scene=dict(xaxis=dict(title='X', backgroundcolor=bgcolor, gridcolor=fontcolor, showbackground=True, zerolinecolor=fontcolor, showgrid=False),
    #                             yaxis=dict(title='Y', backgroundcolor=bgcolor, gridcolor=fontcolor, showbackground=True, zerolinecolor=fontcolor, showgrid=False),
    #                             zaxis=dict(title='Z', backgroundcolor=bgcolor, gridcolor=fontcolor, showbackground=True, zerolinecolor=fontcolor), showgrid=False),
    #                 paper_bgcolor=bgcolor,
    #                 font=dict(color=fontcolor),
    #                 width=800, height=700)

    # # Create a figure and add the trace and layout
    # fig = go.Figure(data=[trace], layout=layout)

    # Return the HTML for the plot using Plotly's embed API
    # return render_template('plot.html', plot=fig.to_html(full_html=False))

# # Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)