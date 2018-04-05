import numpy as np
import pandas as pd
import numba
from matplotlib import patches, cm, pyplot

class Model(object):
  """
  Truss model
  """
  def __init__(self):
    self.nodes = []
    self.bars = []
  
  def data(self, at = "nodes"):
    """
    Returns the data associated with the bars/nodes a dataframe.
    
    Inputs:
    
    * at: should be 'nodes' or 'bars'
    
    >>> m.data(at = "nodes")
        block        coords            disp              force       label
        bx     by      x  y           ux           uy    Fx    Fy     o
    0   True   True      0  0            0            0 -2000 -1000     A
    1   True  False      0  1            0   4.7619e-05  1000     0     B
    2  False  False      1  0  9.52381e-05  0.000277544  1000  1000     C
    3  False  False      1  1            0  0.000277544     0     0     D
    
    >>> m.data(at = "bars")
        conn    direction           geometry                props                    \
        c1 c2        dx        dy   length       volume density      mass section   
    0    A  B         0         1        1       0.0001    2700      0.27  0.0001   
    1    A  C         1         0        1       0.0001    2700      0.27  0.0001   
    2    B  C  0.707107 -0.707107  1.41421  0.000141421    2700  0.381838  0.0001   
    3    C  D         0         1        1       0.0001    2700      0.27  0.0001   
    4    B  D         1         0        1       0.0001    2700      0.27  0.0001   
             state                                         
        elongation       strain       stress      tension  
    0   4.7619e-05   4.7619e-05        1e+07         1000  
    1  9.52381e-05  9.52381e-05        2e+07         2000  
    2 -9.52381e-05 -6.73435e-05 -1.41421e+07     -1414.21  
    3 -5.42101e-20 -5.42101e-20 -1.13841e-08 -1.13841e-12  
    4            0            0            0            0  
    """
    out = pd.concat([t.data() for t in getattr(self, at)], axis = 1)
    out = out.transpose()
    return out
  
  def nodes_data(self):
    """
    Returns the data associated with the bars a dataframe.
    """
    out = pd.concat([bar.data() for bar in self.bars], axis = 1)
    out = out.transpose()
    return out
      
  def add_node(self, node, *args, **kwargs):
    """
    Adds a node to the model. If ``node`` is an instance of the ``truss.core.node``, it is added. If ``node`` an length 2 array containing, a node instance is created and ``node`` it is used as coordinates and other arguments can be provided as well.
    
    :param node: node label or node.
    :type node:  array or ``truss.core.node`` instance.
    
    >>> m = truss.core.Model()
    >>> A = m.add_node((1., 3.), label = "A")
    <Node A: x = 1.0, y = 3.0>
    >>> B = truss.core.Node((4., 5.), label = "B")
    >>> m.add_node(B)
    <Node B: x = 4.0, y = 5.0>
    """
    if isinstance(node, Node) == False:
      node = Node(node, *args, **kwargs)
    self.nodes.append(node)  
    return node
  
  def add_bar(self,*args , **kwargs):
    """
    Add a bar to the model.
    
    >>> from truss.core import Node, Bar, Model
    >>> m = Model()
    >>> B = m.add_node((0., 1.), label = "B")
    >>> A = m.add_node((0., 0.), label = "A")
    >>> b = Bar(A, B)
    """
    bar = Bar(*args , **kwargs)
    self.bars.append(bar)
    return bar
  
  def __repr__(self):
    return "<Model: {0} nodes, {1} bars>".format(len(self.nodes), len(self.bars))
    
  def stiffness_matrix(self):
    """
    Returns the full assembled stiffness matrix of the model.
    """
    nodes = np.array(self.nodes)
    bars = self.bars
    nn = len(nodes)
    nb = len(bars)
    K = np.zeros([2 * nn, 2 * nn])
    for b in bars:
      conn = b.conn
      i0 = np.where(nodes == conn[0])[0][0]
      i1 = np.where(nodes == conn[1])[0][0]
      Kb = b.stiffness_matrix()
      Kb_bar = Kb[0:2,0:2]
      K[2*i0:2*i0 +2,2*i0:2*i0 +2] += Kb_bar
      K[2*i1:2*i1 +2,2*i1:2*i1 +2] += Kb_bar
      K[2*i0:2*i0 +2,2*i1:2*i1 +2] -= Kb_bar
      K[2*i1:2*i1 +2,2*i0:2*i0 +2] -= Kb_bar
    return K
    
  
  
  
  def add_force(self, node, magnitude):
    """
    Adds an external force on an existing node.
    
    :param node: node on which the force is added.
    :type node: ``truss.core.Node`` instance.
    :param magnitude: force magnitude on both directions
    :type magnitude: length 2 array.
    """
    magnitude = np.array(magnitude).astype(np.float64)[0:2]
    self.forces.append( (node, magnitude) )
  
  def force_vector(self):
    """
    Returns the full force vector applied on the system.
    """
    nodes = self.nodes
    force_vector = np.array([n.force for n in nodes]).flatten()
    return force_vector
  
  def solve(self):
    """
    Solves the system.
    """
    adof = self.active_dof()
    nodes = self.nodes
    nn = len(nodes)
    u = np.zeros(2 * nn)
    K = self.stiffness_matrix()
    Adof1, Adof0 = np.meshgrid(adof, adof)
    Kr = K[(Adof0, Adof1)]
    f = self.force_vector()
    fr = f[adof]
    u[adof] = np.linalg.solve(Kr,fr)
    nodes = np.array(self.nodes)
    f = np.dot(K, u)
    for i in range(len(nodes)):
      node = nodes[i]
      for j in range(2):
        node.displacement[j] = u[2*i+j]
        if node.block[j]: node.force[j] = f[2*i+j]
          
      
    bars = self.bars
    for bar in bars:
      n0 = bar.conn[0]
      n1 = bar.conn[1]
      bar.elongation = (n1.displacement - n0.displacement).dot(bar.direction())  
      bar.tension = bar.elongation * bar.stiffness()
      bar.strain = bar.elongation / bar.length()
      bar.stress = bar.tension / bar.section 
   
  
  def active_dof(self):
    """
    Returns the indices of the active (i. e. not blocked) degrees of freedom.
    """
    nodes = self.nodes
    nn = len(nodes)
    a = np.ones(2 * nn)
    for i in range(nn):
      if nodes[i].block[0]: a[2 * i    ] = 0 
      if nodes[i].block[1]: a[2 * i + 1] = 0  
    a = np.where(a == 1)[0]
    return a
  
  
  def bbox(self, deformed = True, factor = .2):
    """
    Returns the bounding box of the truss.
    """
    xlim = np.zeros(2)
    ylim = np.zeros(2)
    for n in self.nodes:
      pos = n.coords.copy()
      if deformed: pos += n.displacement
      xlim[0] = min(xlim[0], pos[0])
      xlim[1] = max(xlim[1], pos[0])
      ylim[0] = min(ylim[0], pos[1])
      ylim[1] = max(ylim[1], pos[1])
    d = max(xlim[1]-xlim[0], ylim[1]-ylim[0])   
    xlim[0] -= d*factor
    xlim[1] += d*factor
    ylim[0] -= d*factor
    ylim[1] += d*factor
    return xlim, ylim
  
  def draw(self, ax, deformed = True, field = "stress", label = True, forces = True, displacements = False, force_scale = 1., displacement_scale = 1.):
    """
    Draws the truss in ``matplotlib`` axes.
    
    :param ax: matplotlib axes.
    :type ax: ``matplotlib.axes instance``
    :param deformed: configuration to be plotted.
    :type deformed: Bool
    :param field: field to be plotted. Options are "tension" or "stress".
    :type deformed: String
    :param label: if True, node labels are plotted.
    :type label: Bool
    :param forces: if True, external forces are plotted.
    :type forces: Bool
    :param displacements: if True, displacements are plotted.
    :type displacements: Bool
    :param force_scale: scale of the external forces vector.
    :type force_scale: float
    :param displacement_scale: scale of the external displacement vector.
    :type displacement_scale: float
    
    """
    for node in self.nodes: node.draw(ax, deformed = deformed)
    bars = self.bars
    length = np.array([b.length for b in bars])
    if field != None:
      if field == "stress": 
        values = np.array([b.stress for b in bars])
        cbar_label = "Normal stress, $\sigma$ [Pa]"
      if field == "tension": 
        values = np.array([b.tension for b in bars])
        cbar_label = "Tension, $N$ [N]"
      colors = cm.jet(values)
      vmin = min(0., values.min())
      vmax = max(0., values.max())
      colormap = pyplot.cm.ScalarMappable(cmap=cm.jet, 
        norm=pyplot.Normalize(vmin = vmin, vmax = vmax))
      colormap._A = []
    for i in range(len(bars)):
      if field == None:
        color = None
      else:  
        color = colormap.to_rgba(getattr(bars[i], field))
      bars[i].draw(ax = ax, deformed = deformed, color = color)
    if field != None:
      cbar = pyplot.colorbar(colormap)
      cbar.set_label(cbar_label)    
    F = np.array([node.force for node in self.nodes]).transpose()
    P = np.array([node.coords for node in self.nodes]).transpose()
    U = np.array([node.displacement for node in self.nodes]).transpose()
    if deformed : P += U
    if forces:
      qf = ax.quiver(P[0], P[1], F[0], F[1], scale_units='xy', angles = "xy", pivot="tail", scale=force_scale**-1, color = "red")
      #qk = ax.quiverkey(qf, 0.1, 1.1, 1, r'1 N', labelpos='E')
    if displacements:
      if deformed: 
        upos = "tip"
      else:
        upos = "tail"  
      qu = ax.quiver(P[0], P[1], U[0], U[1], scale_units='xy', angles = "xy", pivot=upos, scale=1., color = "green")
  
  def mass(self):
    return np.array([b.mass() for b in self.bars]).sum()
  
      
class Node(object):
  """
  Creates a node.
  
  :param coords: coordinates of the node.
  :type coords: length 2 float array
  :param force: external force applied on the node.
  :type force: length 2 float array
  :param block: bloked degrees of freedom.
  :type block: length 2 boolean array
  :param label: label of the node.
  :type label: string
  
  >>> from truss.core import Node
  >>> A = Node((1.,5.), label = "A", block = (False, True) )

  """
  def __init__(self, 
      coords = np.array([0., 0.]), 
      label = None, 
      force = np.zeros(2),
      block = np.array([False, False]), 
      block_side = 1):
  
    coords = np.array(coords).astype(np.float64)[0:2]
    self.coords = np.array(coords)
    self.displacement = np.zeros(2)
    self.force = np.array(force)
    self.block = np.array(block)
    self.label = label
    self.block_side = block_side
  
  def data(self):
    """
    Returns the data associated with the node as a pandas.Series object.
    
    >>> A.data()
    block   bx    True
            by    True
    coords  x        0
            y        0
    disp    ux       0
            uy       0
    force   Fx   -2000
            Fy   -1000
    label   o        A
    dtype: object 
    """
    return pd.Series({("label", "o") : self.label,
                      ("coords", "x"): self.coords[0],
                      ("coords", "y"): self.coords[1],
                      ("disp", "ux"): self.displacement[0],
                      ("disp", "uy"): self.displacement[1],
                      ("force", "Fx"): self.force[0],
                      ("force", "Fy"): self.force[1],
                      ("block", "bx"): self.block[0] == 1,
                      ("block", "by"): self.block[1] == 1,
                         })
  
  def __repr__(self):
    return str(self.data())
  
  def draw(self, ax, deformed = True, radius = 0.1, force_factor = 5.):
    """
    Draws the node.
    """
    pos = self.coords.copy()
    if deformed: pos += self.displacement
    patch = patches.Circle(pos, radius, color='k',clip_on=False)
    ax.add_artist(patch)
    if self.block[0]:
      d = radius * 2.
      bs = self.block_side
      verts = np.array([[-.1,0.], [-1.,.9], [-1.,-.9], [-.1, 0.]]) 
      verts *= d
      verts += pos
      p = patches.Polygon(verts, facecolor = "none",clip_on=False, linewidth = 1.5)
      ax.add_artist(p)
      p = patches.Circle(pos + np.array([-1.5, .5])*d, d*.5, facecolor='none',clip_on=False, linewidth = 1.5)  
      ax.add_artist(p) 
      p = patches.Circle(pos + np.array([-1.5, -.5])*d, d*.5, facecolor='none',clip_on=False, linewidth = 1.5)  
      ax.add_artist(p) 
    if self.block[1]:
      d = radius * 2.
      
      verts = np.array([[0.,-.1], [-.9, -1.], [.9,-1.], [0., -.1]]) 
      verts *= d
      verts += pos
      p = patches.Polygon(verts, facecolor = "none",clip_on=False, linewidth = 1.5)
      ax.add_artist(p)
      p = patches.Circle(pos + np.array([-.5, -1.5])*d, d*.5, facecolor='none',clip_on=False, linewidth = 1.5)  
      ax.add_artist(p) 
      p = patches.Circle(pos + np.array([.5, -1.5])*d, d*.5, facecolor='none',clip_on=False, linewidth = 1.5)  
      ax.add_artist(p)   
      
      
    
class Bar(object):
  """
  A bar class.
  
  
  :param n1: start node of the bar.
  :type n1:  ``truss.core.Node`` instance.
  :param n2: end node of the bar.
  :type n2:  ``truss.core.Node`` instance.
  :param section: cross section of the bar.
  :type section:  float
  :param modulus: Young's modulus of the bar's constitutive material.
  :type modulus:  float
  :param density: density of the bar's constitutive material.
  :type density:  float
  :param yield_stress: yield_stress of the bar's constitutive material.
  :type yield_stress:  float
  
  >>> from truss.core import Node, Bar, Model
  >>> m = Model()
  >>> A = m.add_node((0., 1.), label = "A")
  >>> B = m.add_node((1., 1.), label = "B")
  >>> b = Bar(A, B, section = 1., modulus = 210.e9, density = 7800.)
  >>> b
  <Bar: (0.0, 1.0) -> (1.0, 1.0), S = 1.0, E = 2.1e+11, rho = 7800.0>

  """
  def __init__(self, n1, n2, section = 1., modulus = 1., density = 1., 
                     yield_stress = .001):
    
    self.conn = [n1, n2]
    self.section = float(section)
    self.modulus = float(modulus)
    self.density = float(density)
    self.yield_stress = float(yield_stress)
    self.tension = 0.
    self.elongation = 0.
    self.strain = 0.
    self.stress = 0.
  
  def data(self):
    """
    Returns the data associated with the bar as a pandas.Series.
    
    >>> AB.data()
    conn       c1                     A
               c2                     B
    direction  dx                     0
               dy                     1
    geometry   length                 1
               volume            0.0001
    props      density             2700
               mass                0.27
               section           0.0001
    state      elongation    4.7619e-05
               strain        4.7619e-05
               stress             1e+07
               tension             1000
    dtype: object
    """
    return pd.Series({("conn", "c1"): self.conn[0].label,
                      ("conn", "c2"): self.conn[1].label,
                      ("props", "section"): self.section,
                      ("props", "density"): self.density,
                      ("state", "tension"): self.tension,
                      ("state", "elongation"): self.elongation,
                      ("state", "strain"): self.strain,
                      ("state", "stress"): self.stress,
                      ("state", "failure"): (self.yield_stress - abs(self.stress) <= 0.), 
                      ("geometry", "volume"): self.volume(),
                      ("geometry", "length"): self.length(),
                      ("props", "mass"): self.mass(),
                      ("direction", "dx"): self.direction()[0],
                      ("direction", "dy"):self.direction()[1],
                      })
    
  def __repr__(self):
    return str(self.data())
  
  def draw(self, ax, deformed = True, offset = .5, width = .1, color = None):
    b = self
    o = offset
    w = width
    l = b.length(deformed)
    n0,n1 = b.conn[0].coords.copy(), b.conn[1].coords.copy()
    if deformed:
      n0 += b.conn[0].displacement
      n1 += b.conn[1].displacement
    u = b.direction(deformed)
    n = b.normal(deformed)
    verts = np.array([ n0, n0 + o*u, n0 + (o+w)*u + w*n, 
      n0 + (l-o-w)*u + w*n, n0 + (l-o)*u, n0 + l*u, n0 + (l-o)*u,
      n0 + (l-o-w)*u - w*n, n0 + (o+w)*u - w*n, n0 + o*u, n0])
    tension = b.tension
    if color == None: color = "none"
    p = patches.Polygon(verts, facecolor = color, linewidth = 1.5, 
                        edgecolor = "black",clip_on=False)
    ax.add_artist(p)  
   
  def length(self, deformed = False):
    """
    Returns the length of the bar.
    
    :param deformed: False for undeformed configuration, True for deformed configuration.
    :type deformed: Bool
    :rtype: float
    """
    conn = self.conn
    if deformed:
      return ((conn[0].coords + conn[0].displacement 
        - conn[1].coords - conn[1].displacement)**2).sum()**.5 
    else:
      return ((conn[0].coords - conn[1].coords)**2).sum()**.5 
   
     
  def volume(self):
    """
    Returns the (undeformed) volume of the bar.
    
    :rtype: float
    """
    S = self.section
    L = self.length()
    return S * L
  
  
  def mass(self):
    """
    Returns the mass of the bar.
    
    :rtype: float
    """
    V = self.volume()
    rho = self.density
    return V * rho
  
  
  def stiffness(self):
    """
    Returns the stiffness of the bar.
    
    :rtype: float
    """
    S = self.section
    L = self.length()
    E = self.modulus
    return E * S / L    
  
  
  def direction(self, deformed = False):
    """
    Returns the unit vector corresponding to the direction of the bar from start to end.
    
    :rtype: length 2 array
    """
    conn = self.conn
    if deformed:
      return (conn[1].coords + conn[1].displacement 
        - conn[0].coords - conn[0].displacement) / self.length(deformed)
    else:
      return (conn[1].coords - conn[0].coords) / self.length(deformed)
  
  
  def normal(self, deformed = False):
    """
    Returns the unit vector corresponding to the normal direction of the bar.
    
    :rtype: length 2 array
    """
    t = self.direction(deformed)
    n = np.zeros(2)
    n[0] = -t[1]
    n[1] = t[0]
    return n
  
  def stiffness_matrix(self):
    """
    Returns stiffness matrix of the bar.
    
    :rtype: (4,4) array
    
    >>> from truss.core import Node, Bar, Model
    >>> m = Model()
    >>> B = m.add_node((0., 1.), label = "B")
    >>> A = m.add_node((0., 0.), label = "A")
    >>> b = Bar(A, B)
    >>> b.stiffness_matrix()
    array([[ 0.,  0.,  0.,  0.],
           [ 0.,  1.,  0., -1.],
           [ 0.,  0.,  0.,  0.],
           [ 0., -1.,  0.,  1.]])

    """
    u = self.direction()
    k = self.stiffness()
    ux, uy = u[0], u[1]
    a = np.array([[-ux, -uy, ux, uy]])
    K = k *  a.transpose().dot(a)
    return K
  
          
