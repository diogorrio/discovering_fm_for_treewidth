# Minimal Forbidden Minors for Distinct Treewidths

Project code developed to accompany the thesis of the bachelor programme BSc Data Science and Artificial Intelligence, 
taught by Universiteit Maastricht. 
It consists in (re-)discovering Minimal Forbidden Minors for Treewidth, 
through a series of graph generation/analysis techniques.

### Abstract
The aim of this thesis is to explore the efficiency of algorithms dedicated to finding minimal forbidden minors in 
F(4), where F(k) is the finite set of graphs with the following property: a graph G has treewidth at most k if and 
only if none of the graphs in F(k) are a minor of G. The treewidth of a graph is a fundamental characteristic that 
describes its resemblance to a tree. This is crucial in graph theory, as it enables polynomial time solutions for 
NP-hard problems, for graphs with bounded treewidth. Methods of communicating the discovered forbidden minors to the 
community in a verifiable manner are developed, as only up the set F(3) are they fully known. Finally, the research 
aims to analyze the exhaustiveness of the obtained list of forbidden minors in F(4), as well as examine the 
feasibility of extending the algorithms used in F(4) in generating a non-exhaustive list for F(5).

To achieve these goals, the study employs graph generation and exploration techniques, search-space pruning methods, and 
connectivity and isomorphism checks. Different approaches are evaluated, and a MySQL database structure is implemented 
to facilitate the sharing of any research outcomes.

It defines an endeavor to advance the field of algorithmic 
graph theory and its possible applications in solving complex computational problems.


### Run Instructions
// Empty.

### Version Log
V1. Build the initial structure of the project.\
V2. List possible approaches to finding the forbidden minors.\
V3. Implementation of MySQL database structure and functions.\
V4. Synced the thesis report under documents.\
V5. Brute-force approach on generating all connected non-isomorphic graphs of n vertices (i.e. graphs fit for analysis)
AND algorithmic skeleton of finding forbidden minors.\
V6. Combinatorial enumeration approach implemented.\
V7. Binomial graph random sampling approach implemented, given the lack of feasibility 
of the brute-force graph generation process.\
V8. Combined approach (combinatorial enumeration up to 7 vertices AND random sampling thereon) implemented.\
V9. Integrated exact treewidth solver and isomorphism checker.\
V10. Experiment design.\
V11. Upload the minimal forbidden minors found as a database/text file, as well as images.

## LICENSE
See [LICENSE](LICENSE).
