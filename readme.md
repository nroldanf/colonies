# Brief Description of the Algorithm Used

Automatic system for colony counting using DIP techniques.

Process employed so far:

1. `Grayscale conversion`.

2. `Linear contrast enhancement`.

3. `Determination of the petri-dish centers`.
   3.1. Edge detection using the Canny method.
   3.2. Dilation with a diamond-shaped structuring element to better define the circular shapes of the Petri dish wells.
   3.3. Cross-correlation with generated binary circular templates.
   3.4. Finding the centers of the wells by locating them using the petri-dish radius.

4. `Petri-dish segmentation`: verifying all pixels that are within a circle with a specified average radius using the previously obtained centers.

5. `Thresholding`: determining a threshold using Otsu's method, which is scaled by a factor equal to the average of the image, and then applying this threshold to the image.

6. `Segmentation of the colonies from the edges` using Euclidean distance in the CIE L*a*b color space.

7. `Elimination of colonies that do not have more than 50 cells` using geometric properties of the regions.

8. `Labeling and counting`: regions with certain connectivity are labeled and then counted.
