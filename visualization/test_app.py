from flask import Flask, render_template
import plotly.graph_objs as go
import numpy as np

# Create a Flask application
app = Flask(__name__)

# Define a route for the webpage
@app.route('/')
def index():
    # Generate some random data
    x, y, z = np.random.multivariate_normal([0,0,0], np.eye(3), 500).transpose()

    # Create a 3D scatter plot
    trace = go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=5, color=z, colorscale='Viridis', opacity=0.8))

    # Create a layout for the plot
    layout = go.Layout(scene=dict(xaxis=dict(title='X'), yaxis=dict(title='Y'), zaxis=dict(title='Z')), width=800, height=700)

    # Create a figure and add the trace and layout
    fig = go.Figure(data=[trace], layout=layout)

    # Return the HTML for the plot using Plotly's embed API
    return render_template('plot.html', plot=fig.to_html(full_html=False))

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)