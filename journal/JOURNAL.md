---
title: 'OpenPFO: A Python workflow for CFD based design space exploration and optimization'
tags:
  - Python
  - Computational Fluid Dynamics
  - OpenFOAM
  - Design Space Exploration
  - Optimization
authors:
  - name: Emma Lee Keeping
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    affiliation: 1 # (Multiple affiliations must be quoted)
  - name: Thomas Kim
    equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    affiliation: 1
  - name: Kate Armstrong
    equal-contrib: true
    affiliation: 1
affiliations:
 - name: University of Waterloo, Waterloo, Ontario, Canada
   index: 1
   ror: 00hx57361 # not sure if this is a UW required thing? Ask JPH
date: 13 August 2017
bibliography: paper.bib
---

# Summary

Engineering design relies more and more on Computational Fluid Dynamics (CFD) 
as a means of validating and improving designs. This process involves four major
steps: geometry generation, meshing, solving, and postprocessing. Conducting 
design optimization using CFD requires repetition of most or all of these steps.

`OpenPFO` (Open source Parametric Flow Optimizer) is a python workflow that 
integrates these four steps, and incorporates an optimization loop. The 
workflow integrates leading open source software for each step, including 
FreeCAD, OpenVSP, OpenFOAM, and Paraview softwares with the Pymoo optimization 
library. The final product is one which is capable of accepting a parametric 
geometry, simulation case, optimization objectives, and parameter ranges, 
iterating through the design space to provide the final, optimized result. 

# Statement of need

`OpenPFO` is a Python workflow to conduct CFD based design space exploration and
optimization. The workflow interconnects the four main steps of CFD analysis: 
geometry generation, meshing, solving, and post processing within an overall 
optimization algorithm. The purpose of the workflow is to streamline CFD informed
design optimization, allowing specified parameters to be motified automatically, 
and the geometry reran using a specified simulation case. 

This workflow replaces a heavily manual process wherein once a geometry has
been ran in CFD and post processed, a new geometry will need to be brought
through the overall generation, meshing, solving, and postprocessing steps.
This approach can be very time consuming and is a major barrier to CFD based
design optimization. `OpenPFO` streamlines this process, eliminating the repetitve 
steps and guesswork in the typical process, allowing engineers to focus on 
more critical areas and exploring a wider design space. 

# State of the field        

There are several tools which complete the goal of `OpenPFO`:
SU2
HEEDS
VSP
Luminary Cloud
NTOP

While each of these tools accomplish some or all of the goals of `OpenPFO`, each
have at least one of two notable problems, cost, and extensibility. `OpenPFO`,
through its integration with entirely open source resources, is free of cost to 
access and operate. The manner in which `OpenPFO` has beed developed, makes it
easy to integrate new softwares provided they posess a Python interface. This 
makes it extensible to a variety of physics problems, allowing specialized 
software such as `OpenVSP` for aerospace design to be used. Established 
integration with `OpenFOAM`, a well known CFD solver, allows for inherent
extensibility as well, allowing researchers to quickly implement their 
established simulation cases. 

# Software design

`OpenPFO`'s structure has been formed with the intention of acting as the link
between established software and completing the loop between the steps with
the implementation of an optimization step. # Talk about the flowchart here 

# Research impact statement

`OpenPFO`has been deveoped with the intention of improving the flow of the 
engineering design process. Through its development, it has been made clear that
it has immense potential for research impact. While it was validated with a 
simple delta wing aircraft design, a secondary case of hypersonic busemann intake
optimization has been introduced. The application to this type of problem, 
enforces its research impact potential as it provides an opportunity to research
previously unconsidered optimization of regimented intake designs with the ability
to focus on key issues such as intake cross flow which can significantly decrease
combustor performance. 


# Mathematics # This is template

Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}
and refer to \autoref{eq:fourier} from text.

# Citations # This is template

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures # This is template

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# AI usage disclosure # This is template

No generative AI tools were used in the development of this software, the writing
of this manuscript, or the preparation of supporting materials.

# Acknowledgements # This is template

We would like to acknowledge the support and guidance provided by our 
advisors, Dr. Jean-Pierre Hickey (University of Waterloo MPI Lab) and 
Dr. Jimmy-John Hoste (Destinus Aerospace). The development and validation 
of `OpenPFO` was conducted with technical and user input from the 
University of Waterloo WatArrow Student Design Team, and the usage of the 
University of Waterloo Nibi Supercomputer though the MPI Lab. 

# References