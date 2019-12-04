# Spotify Billboard Classifier
## DATA1030 project
### Course project for DATA 1030 @ Brown University

In this report, an attempt has been made to predict whether a particular song will
appear in the US top 200 billboard based on the songs given it’s acoustic features.

## Data Sources

1. Kaggle - [The Billboard 200 acoustic data](https://www.kaggle.com/snapcrack/the-billboard-200-acoustic-data) (for songs in the billboard)
2. [Spotipy](https://spotipy.readthedocs.io/en/latest/) - The Python Spotify API


## Acoustic Features

The entire description of the Spotify EchoNest acoustic features can be obtained in the following [link](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/)

## Classification Algorithms Used
- Random Forest Classification
- XGBoost Classification
- AdaBoost CLassification

## Confusion Matrices
<html>
 <div class="row">
  <div class="column">
    <img src="/figures/randomforest_cm_normed.png" alt="Snow" style="width:33%">
  </div>
  <div class="column">
    <img src="/figures/xgboost_cm_normed.png" alt="Forest" style="width:33%">
  </div>
  <div class="column">
    <img src="/figures/adaboost_cm_normed.png" alt="Mountains" style="width:33%">
  </div>
</div> 
</html>

## Rooms for improvement

The dataset is highly imbalanced, and the features of the two classes are heavily overlapping. 
The algorithm to obtain the non-billboard songs was flawed and needs a heavy improvement. 
Also certain algorithms such as Support Vector Machines and Deep Learning techniques were not applied due to lack of time and expertise.
I wish to come back to this in the future and refine it.

If you are interested, feel free to fork.
