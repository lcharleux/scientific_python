.. Note::

  This notebook can be downloaded here: :download:`Basics.ipynb <../../notebooks/0_Python/Basics.ipynb>` 


.. codeauthor:: Ludovic Charleux ludovic.charleux@univ-smb.fr

Python Basics
=============

Variables and simple types
--------------------------

.. code:: ipython3

    2 + 2 # Addition of 2 numbers




.. parsed-literal::

    4



.. code:: ipython3

    a = 5 # An integer
    a




.. parsed-literal::

    5



.. code:: ipython3

    type(a) # Get "a"'s class.




.. parsed-literal::

    int



.. code:: ipython3

    type(5.) # A floating point number




.. parsed-literal::

    float



.. code:: ipython3

    type("Hello") # A string




.. parsed-literal::

    str



.. code:: ipython3

    type(True)




.. parsed-literal::

    bool



.. code:: ipython3

    type(None)




.. parsed-literal::

    NoneType



Containers
----------

Lists
~~~~~

.. code:: ipython3

    l = [1, 3, "cat"] # A list that contained both ints and strings.
    l




.. parsed-literal::

    [1, 3, 'cat']



.. code:: ipython3

    l[0] # Python counts from 0 !




.. parsed-literal::

    1



.. code:: ipython3

    l[1] = 8
    l




.. parsed-literal::

    [1, 8, 'cat']



.. code:: ipython3

    l.append("dog")
    l




.. parsed-literal::

    [1, 8, 'cat', 'dog']



.. code:: ipython3

    len(l)




.. parsed-literal::

    4



Dictionnaries
~~~~~~~~~~~~~

.. code:: ipython3

    d = {"tomato":"red", "banana": "yellow"} # A dictionnary
    d




.. parsed-literal::

    {'banana': 'yellow', 'tomato': 'red'}



.. code:: ipython3

    d.keys()




.. parsed-literal::

    dict_keys(['tomato', 'banana'])



.. code:: ipython3

    d.values()




.. parsed-literal::

    dict_values(['red', 'yellow'])



.. code:: ipython3

    d["tomato"]




.. parsed-literal::

    'red'



.. code:: ipython3

    d["salad"] = "green"
    d




.. parsed-literal::

    {'banana': 'yellow', 'salad': 'green', 'tomato': 'red'}



Looping
-------

.. code:: ipython3

    for a in [1, 2, "hello"]:
        print(a) # Leading spaces (indentations) are mandatory to define code blocks


.. parsed-literal::

    1
    2
    hello


.. code:: ipython3

    for i in range(5):
        print(i**2)


.. parsed-literal::

    0
    1
    4
    9
    16


.. code:: ipython3

    a = 5
    if a < 4:
        print("a<4")
    else:
        print("a>4")


.. parsed-literal::

    a>4


.. code:: ipython3

    a = 0
    while a < 5:
        print("hello")
        a += 2


.. parsed-literal::

    hello
    hello
    hello


Functions
---------

**Funnctions** are objets that take **arguments** and possibly:

-  **Return** something,
-  Modify their arguments.

.. code:: ipython3

    def myFunction(x, a = 1, b = 0.):
        """
        My Function: Affine equation 
        
        * Params: x, a, b: 3 numbers
        * Returns: y = a*x + b
        """
        return a* x + b

.. code:: ipython3

    myFunction(1) # a and b have default values 




.. parsed-literal::

    1.0



.. code:: ipython3

    myFunction(1, 2, 3)




.. parsed-literal::

    5



.. code:: ipython3

    myFunction(x = 1, b = 4) # Arguments are defined by keywords




.. parsed-literal::

    5



Classes
-------

**Classes** define objects that, onces instanciated can perform many
tasks. After some work, classes are an efficient way to structure your
work.

.. code:: ipython3

    class Vector3D:
        """
        A very simple 3D vector class. 
        """
        def __init__(self, x = 0, y = 0., z = 0.):
            self.x = x
            self.y = y
            self.z = z
        
        def __repr__(self):
            return "<Vector: ({0:.2e}, {1:.2e}, {2:.2e})>".format(self.x, self.y, self.z)
        
        def norm(self):
            """
            Returns the norm of the vector.
            """
            return (self.x**2 + self.y**2 + self.z**2)**.5
        
        def normalize(self):
            """
            Divides the vector by its own norm.
            """
            n = self.norm()
            self.x /= n
            self.y /= n
            self.z /= n
            
        def cross(self, other):    
            """
            Cross product with another vector.
            """
            return Vector3D(x = self.y * other.z - self.z * other.y,
                            y = self.z * other.x - self.x * other.z,
                            z = self.x * other.y - self.y * other.x)
        __mul__ = cross
            


.. code:: ipython3

    v = Vector3D(2,2,0)
    v




.. parsed-literal::

    <Vector: (2.00e+00, 2.00e+00, 0.00e+00)>



.. code:: ipython3

    v.norm()




.. parsed-literal::

    2.8284271247461903



.. code:: ipython3

    v.normalize()
    v




.. parsed-literal::

    <Vector: (7.07e-01, 7.07e-01, 0.00e+00)>



.. code:: ipython3

    v.norm()




.. parsed-literal::

    0.9999999999999999



.. code:: ipython3

    u = Vector3D(0,0,1) # Cross product
    v.cross(u)




.. parsed-literal::

    <Vector: (7.07e-01, -7.07e-01, 0.00e+00)>



.. code:: ipython3

    u * v # operator overcharge




.. parsed-literal::

    <Vector: (-7.07e-01, 7.07e-01, 0.00e+00)>


