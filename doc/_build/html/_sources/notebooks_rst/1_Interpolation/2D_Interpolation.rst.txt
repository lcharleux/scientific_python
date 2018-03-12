.. Note::

  This notebook can be downloaded here: :download:`2D_Interpolation.ipynb <../../notebooks/1_Interpolation/2D_Interpolation.ipynb>` 


.. code:: ipython2

    from IPython.core.display import HTML
    def css_styling():
        styles = open('styles/custom.css', 'r').read()
        return HTML(styles)
    css_styling()




.. raw:: html

    <link href='http://fonts.googleapis.com/css?family=Fenix' rel='stylesheet' type='text/css'>
    <link href='http://fonts.googleapis.com/css?family=Alegreya+Sans:100,300,400,500,700,800,900,100italic,300italic,400italic,500italic,700italic,800italic,900italic' rel='stylesheet' type='text/css'>
    <link href='http://fonts.googleapis.com/css?family=Source+Code+Pro:300,400' rel='stylesheet' type='text/css'>
    <style>
    
    @font-face {
        font-family: "Computer Modern";
        src: url('http://mirrors.ctan.org/fonts/cm-unicode/fonts/otf/cmunss.otf');
    }
    
    
    #notebook_panel { /* main background */
        background: rgb(245,245,245);
    }
    
    div.cell { /* set cell width */
        width: 750px;
    }
    
    div #notebook { /* centre the content */
        background: #fff; /* white background for content */
        width: 1000px;
        margin: auto;
        padding-left: 0em;
    }
    
    #notebook li { /* More space between bullet points */
    margin-top:0.8em;
    }
    
    /* draw border around running cells */
    div.cell.border-box-sizing.code_cell.running { 
        border: 1px solid #111;
    }
    
    /* Put a solid color box around each cell and its output, visually linking them*/
    div.cell.code_cell {
        background-color: rgb(256,256,256); 
        border-radius: 0px; 
        padding: 0.5em;
        margin-left:1em;
        margin-top: 1em;
    }
    
    
    div.text_cell_render{
        font-family: 'Alegreya Sans' sans-serif;
        line-height: 140%;
        font-size: 125%;
        font-weight: 400;
        width:600px;
        margin-left:auto;
        margin-right:auto;
    }
    
    /* Formatting for header cells */
    .text_cell_render h1 {
        font-family: 'Alegreya Sans', sans-serif;
        font-style:regular;
        font-weight: 200;    
        font-size: 50pt;
        line-height: 100%;
        color:#CD2305;
        margin-bottom: 0.5em;
        margin-top: 0.5em;
        display: block;
    }	
    .text_cell_render h2 {
        font-family: 'Fenix', serif;
        font-size: 22pt;
        line-height: 100%;
        margin-bottom: 0.1em;
        margin-top: 0.3em;
        display: block;
    }	
    
    .text_cell_render h3 {
        font-family: 'Fenix', serif;
        margin-top:12px;
    	font-size: 16pt;
        margin-bottom: 3px;
        font-style: regular;
    }
    
    .text_cell_render h4 {    /*Use this for captions*/
        font-family: 'Fenix', serif;
        font-size: 2pt;
        text-align: center;
        margin-top: 0em;
        margin-bottom: 2em;
        font-style: regular;
    }
    
    .text_cell_render h5 {  /*Use this for small titles*/
        font-family: 'Alegreya Sans', sans-serif;
        font-weight: 300;
        font-size: 16pt;
        color: #CD2305;
        font-style: italic;
        margin-bottom: .5em;
        margin-top: 0.5em;
        display: block;
    }
    
    .text_cell_render h6 { /*use this for copyright note*/
        font-family: 'Source Code Pro', sans-serif;
        font-weight: 300;
        font-size: 9pt;
        line-height: 100%;
        color: grey;
        margin-bottom: 1px;
        margin-top: 1px;
    }
    
        .CodeMirror{
                font-family: "Source Code Pro";
    			font-size: 90%;
        }
    /*    .prompt{
            display: None;
        }*/
    	
        
        .warning{
            color: rgb( 240, 20, 20 )
            }  
    </style>
    <script>
        MathJax.Hub.Config({
                            TeX: {
                               extensions: ["AMSmath.js"], 
                               equationNumbers: { autoNumber: "AMS", useLabelIds: true}
                               },
                    tex2jax: {
                        inlineMath: [ ['$','$'], ["\\(","\\)"] ],
                        displayMath: [ ['$$','$$'], ["\\[","\\]"] ]
                    },
                    displayAlign: 'center', // Change this to 'center' to center equations.
                    "HTML-CSS": {
                        styles: {'.MathJax_Display': {"margin": 4}}
                    }
            });
    </script>




2D Interpolation (and above)
============================

Scope
-----

-  Finite number :math:`N` of data points are available:
   :math:`P_i = (x_i, y_i)` and associated values :math:`z_i` ,
   :math:`i \in \lbrace 0, \ldots, N \rbrace`
-  ND interpolation differs from 1D interpolation because the notion of
   neighbourhood is less obvious.

https://en.wikipedia.org/wiki/Interpolation

.. code:: ipython2

    # Setup
    %matplotlib inline
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib
    params = {'font.size'     : 14,
              'figure.figsize':(15.0, 8.0),
              'lines.linewidth': 2.,
              'lines.markersize': 15,}
    matplotlib.rcParams.update(params)


Let’s do it with Python
-----------------------

.. code:: ipython2

    Ni = 40
    Pi = np.random.rand(Ni, 2)
    Xi, Yi = Pi[:,0], Pi[:,1]
    Zi = np.random.rand(Ni)
    
    
    import matplotlib as mpl
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    
    ax.plot(Xi, Yi, Zi, "or", label='Data')
    ax.legend()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()




.. image:: ../../notebooks_rst/1_Interpolation/2D_Interpolation_files/../../notebooks_rst/1_Interpolation/2D_Interpolation_4_0.png


Neighbours and connectivity: Delaunay mesh
------------------------------------------

Triangular mesh over a convex domain

.. code:: ipython2

    from scipy.spatial import Delaunay
    Pi = np.array([Xi, Yi]).transpose()
    tri = Delaunay(Pi)
    plt.triplot(Xi, Yi , tri.simplices.copy())
    plt.plot(Xi, Yi, "or", label = "Data")
    plt.grid()
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()



.. image:: ../../notebooks_rst/1_Interpolation/2D_Interpolation_files/../../notebooks_rst/1_Interpolation/2D_Interpolation_6_0.png


## Interpolation

.. code:: ipython2

    N = 100
    x = np.linspace(0., 1., N)
    y = np.linspace(0., 1., N)
    X, Y = np.meshgrid(x, y)
    P = np.array([X.flatten(), Y.flatten() ]).transpose()
    plt.plot(Xi, Yi, "or", label = "Data")
    plt.triplot(Xi, Yi , tri.simplices.copy())
    plt.plot(X.flatten(), Y.flatten(), "g,", label = "Z = ?")
    plt.legend()
    plt.grid()
    plt.show()



.. image:: ../../notebooks_rst/1_Interpolation/2D_Interpolation_files/../../notebooks_rst/1_Interpolation/2D_Interpolation_8_0.png



Nearest interpolation
---------------------

.. code:: ipython2

    from scipy.interpolate import griddata
    Z_nearest = griddata(Pi, Zi, P, method = "nearest").reshape([N, N])
    plt.contourf(X, Y, Z_nearest, 50)
    plt.plot(Xi, Yi, "or", label = "Data")
    plt.colorbar()
    plt.legend()
    plt.grid()
    plt.show()



.. image:: ../../notebooks_rst/1_Interpolation/2D_Interpolation_files/../../notebooks_rst/1_Interpolation/2D_Interpolation_11_0.png


Linear interpolation
--------------------

.. code:: ipython2

    from scipy.interpolate import griddata
    Z_linear = griddata(Pi, Zi, P, method = "linear").reshape([N, N])
    plt.contourf(X, Y, Z_linear, 50, cmap = mpl.cm.jet)
    plt.colorbar()
    plt.contour(X, Y, Z_linear, 10, colors = "k")
    #plt.triplot(Xi, Yi , tri.simplices.copy(), color = "k")
    plt.plot(Xi, Yi, "or", label = "Data")
    plt.legend()
    plt.grid()
    plt.show()



.. image:: ../../notebooks_rst/1_Interpolation/2D_Interpolation_files/../../notebooks_rst/1_Interpolation/2D_Interpolation_13_0.png


Higher order interpolation
--------------------------

.. code:: ipython2

    from scipy.interpolate import griddata
    Z_cubic = griddata(Pi, Zi, P, method = "cubic").reshape([N, N])
    plt.contourf(X, Y, Z_cubic, 50, cmap = mpl.cm.jet)
    plt.colorbar()
    plt.contour(X, Y, Z_cubic, 20, colors = "k")
    #plt.triplot(Xi, Yi , tri.simplices.copy(), color = "k")
    plt.plot(Xi, Yi, "or", label = "Data")
    plt.legend()
    plt.grid()
    plt.show()



.. image:: ../../notebooks_rst/1_Interpolation/2D_Interpolation_files/../../notebooks_rst/1_Interpolation/2D_Interpolation_15_0.png


Comparison / Discussion
-----------------------

.. code:: ipython2

    levels = np.linspace(0., 1., 50)
    fig = plt.figure()
    ax =  fig.add_subplot(1, 3, 1)
    plt.contourf(X, Y, Z_nearest, levels)
    plt.grid()
    ax =  fig.add_subplot(1, 3, 2)
    plt.contourf(X, Y, Z_linear, levels)
    plt.grid()
    ax =  fig.add_subplot(1, 3, 3)
    plt.contourf(X, Y, Z_cubic, levels)
    plt.grid()



.. image:: ../../notebooks_rst/1_Interpolation/2D_Interpolation_files/../../notebooks_rst/1_Interpolation/2D_Interpolation_17_0.png


