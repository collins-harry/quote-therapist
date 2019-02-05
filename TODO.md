# TODO

## App

- [X] build app 
  - [X] Eliza  
  - [X] scrollbar
  - [X] focus on message box
  - [X] integrate semi-data
  - [X] image placement
- [X] put on heroku
  - [X] put glove on heroku

## SEMI

- [X] scrap quotes
- [ ] scrap images for small quote database
 
## Stats for Nerds

- [ ] Distribution of vector distances
- [ ] 2d representation (PCA)
- [ ] plot gephi with parameters;
  - [ ] vector distances
  - [ ] vector

## Wish

- [ ] integrate quotes (small, medium, large)
- [ ] make suitable for phone (set max-width and remove percentages)

## Other todo

- [X] remove username box
- [X] make GloVe fit in repo

## Other

saved docvectors and which ones to use are in qoute_mapper.py (getDocvectors())

### SfN

clustered docvectors together using k-means algorithm, chose 50 clusters.
Attempts to use the 'elbow' method by plotting sum of squared errors (SSE) over the cluster number and looking for a kink in the curve.
Unfortunately there was no kink implying the docvectors are not heavily clustered. 
This is ok as our interest in clustering the data is to make the distribution and visualisations more manageable for the viewer. 

https://plot.ly/matplotlib/line-charts/#setting-marker-size-in-matplotlib
