import numpy as np


def extract_central_gravity(heatmap):
  # Normalize heatmap data
  heatmap = (heatmap - np.min(heatmap)) / (np.max(heatmap) - np.min(heatmap))

  # Initialize x and y axis arrays
  x_axis = np.zeros(heatmap.shape[1])
  y_axis = np.zeros(heatmap.shape[0])

  # Loop through each row and column of heatmap data
  for i in range(heatmap.shape[0]):
      for j in range(heatmap.shape[1]):
          x_axis[j] += heatmap[i][j] * j
          y_axis[i] += heatmap[i][j] * i

  # Divide x_axis and y_axis by the sum of the heatmap data
  x_axis /= np.sum(heatmap)
  y_axis /= np.sum(heatmap)

  # Central gravity coordinates
  cg_x = np.sum(x_axis)
  cg_y = np.sum(y_axis)
  return cg_x, cg_y
