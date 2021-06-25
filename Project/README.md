##Links
- [bl.ocks](http://bl.ocks.org/chrisrzhou/d5bdd8546f64ca0e4366) 
- [plunker](http://embed.plnkr.co/TgGw0V/preview)

##Description
- D3 Sunburst Sequence visualizes a graph of nodes by highlight sequential progression of nodes leading up to a final value.  It is useful to visualize relative weights/percentages of a starting state to an end state (e.g. webpage redirects, product retention, subscription-based products, cashflows).
- This is a variation of the original [sunburst sequence](http://bl.ocks.org/kerryrodden/7090426).
- A major improvement to the original vis is to organize the code base and draw the D3 components (breadcrumbs, sunburst, legend) from a single HTML div tag, and to dynamically assign color and legend scales.
- The other improvement is generalizing and conventionalizing data inputs. The input requires a simple tabular schema of `sequence, stage, node, value` (see below) and the program will parse the data into a JSON graph.
- The CSV data can be unsorted but it must NOT contain a header.
- The data input has to be a 4-column CSV conforming to the data schema of:
  - `sequence (int/string)`: an ordered sequence that clearly defines the grouping of nodes.
  - `stage (int)`: the index/order of nodes in a given sequence.
  - `node (int/string)`: the data name of the node.
  - `value (int)`: the value at each stage of a given sequence. Only the final stage value in a given sequence is used in this visualization.

##Files
- **`index.html`**: Main angular app connecting the D3 vis through an angular directive `<sunburst>`.
- **`app.js`**: Main angular app file connecting the DOM view with Javascript variables.  Contains directive `onReadFile` to handle file uploads and `sunburst` to re-render the D3 visualization on data updates.
- **`sunburst.js`**: Contains the logic for drawing the D3 visualization by selecting the `angular.element` from which the vis is to be drawn.  Updates and prompts D3 to re-render the visualization when the angular data changes on file uploads.
- **`style.css`**: stylesheet containing optional D3 classes that can be adjusted (commented out)
- **`data.csv`**: Four CSV-data files for sample downloads and uploads to the app.

##Notes
- Visualization hover can be a little glitchy if the base data does not contain very meaningful sequences i.e. smaller parent nodes that lead up to larger child nodes.
- A big help from this [fiddle](http://jsfiddle.net/alexsuch/6aG4x/) to help implement an AngularJS `FileReader`.