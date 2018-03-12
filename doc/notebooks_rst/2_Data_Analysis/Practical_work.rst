.. Note::

  This notebook can be downloaded here: :download:`Practical_work.ipynb <../../notebooks/2_Data_Analysis/Practical_work.ipynb>` 


.. code:: ipython3

    #Setup
    %load_ext autoreload
    %matplotlib nbagg
    %autoreload 2
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib as mpl


.. parsed-literal::

    The autoreload extension is already loaded. To reload it, use:
      %reload_ext autoreload


Practical work: take a look at the French Road Safety Data base
===============================================================

The purpose of this session is to highlight some data of this base using
the panda module.

The data can be downloaded at the following address :
https://www.data.gouv.fr/fr/datasets/base-de-donnees-accidents-corporels-de-la-circulation/#\_

The needed files are also available in the DATA directory attached to
this notebook.

The data base is split in 4 files, the following ones will be used :

-  “caracteristiques_2016.csv” : gives global characteristics of the
   accident
-  “usagers_2016.csv” : gives information on the involved people
-  “lieux_2016.csv” : gives information on the location

A detailed description of the base is given in the documentation :
“Description_des_bases_de_donnees_ONISR_-Annees_2005_a_2016.pdf” (in
French)

Questions
---------

**Question 1**: Load the 3 data bases and observe the different fields.
Which one is common to all data base ? Concatenat the 3 data base in one
? (use de concat commande of panda)



**Question 2**: What is the ratio between male and female involved in an
accident ? Show results in a graphical way.


**Question 3**: What is the ratio between male and female involved in
accident considering only the driver ? Show results in a graphical way.


**Question 4**: Propose a graphical representation to highlight the age
of the involved victim. (first you should compute the age of the person)


**Question 5**: What is the ratio between male and female involved in
accident considering all victims expect the driver ? Show results in a
graphical way.


**Question 6**: Propose a graphical representation to highlight the
geographical position on each accident which has taken place on the
metropolitan territory.



**Question 7**: What is the ratio between accidents taking place during
the day, night, and transition day/night ? Show results in a graphical
way.

