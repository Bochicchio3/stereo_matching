#%%
from sklearn.svm import LinearSVC
from imutils import paths
import argparse
import cv2
import os
import matplotlib.pyplot as plt
from skimage import feature
import numpy as np
import matplotlib.image as mpimg

#%%

class LocalBinaryPatterns:
	def __init__(self, numPoints, radius):
		# store the number of points and radius
		self.numPoints = numPoints
		self.radius = radius

	def describe(self, image, eps=1e-7):
		# compute the Local Binary Pattern representation
		# of the image, and then use the LBP representation
		# to build the histogram of patterns
		lbp = feature.local_binary_pattern(image, self.numPoints,
			self.radius, method="uniform")
		(hist, _) = np.histogram(lbp.ravel(),
			bins=np.arange(0, self.numPoints + 3),
			range=(0, self.numPoints + 2))

		# normalize the histogram
		hist = hist.astype("float")
		hist /= (hist.sum() + eps)

		# return the histogram of Local Binary Patterns
		return hist
#%%

# initialize the local binary patterns descriptor along with
# the data and label lists
desc = LocalBinaryPatterns(24, 8)
data = []
labels = []
#%%

# loop over the training images
for imagePath in paths.list_images('/home/alfredo/Desktop/PROJECTS/Master Thesis/opencv/images/local_binary_patterns/training'):
	# load the image, convert it to grayscale, and describe it
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	hist = desc.describe(gray)

	# extract the label from the image path, then update the
	# label and data lists
	labels.append(imagePath.split(os.path.sep)[-2])
	data.append(hist)
#%%
 
# train a Linear SVM on the data
model = LinearSVC(C=100.0, random_state=42)
model.fit(data, labels)

#%% 

# loop over the testing images
for imagePath in paths.list_images('images/testing'):
	# load the image, convert it to grayscale, describe it,
	# and classify it
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	hist = desc.describe(gray)
	prediction = model.predict(hist.reshape(1, -1))

	# display the image and the prediction
	cv2.putText(image, prediction[0], (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
		1.0, (0, 0, 255), 3)
	cv2.imshow("Image", image)
	cv2.waitKey(0)
cv2.destroyAllWindows()

# %%
# plt.figure()
# for i in range (0,16):
# 		plt.subplot(4,4,i+1)	
# 		plt.hist(data[i],256)
# plt.show()
img=[]
plt.figure()
counter=0
for i in impaths: 
	img.append( mpimg.imread(impaths[counter]))
	plt.subplot(4,4,counter+1)	
	plt.imshow(img[counter])
	counter+=1
plt.show()

# np.hstack()


#%% 
impaths=[]
for imagePath in paths.list_images('/home/alfredo/Desktop/PROJECTS/Master Thesis/opencv/images/local_binary_patterns/training'):
	impaths.append(imagePath)

# %%
plt.figure()

plt.show()

# %%
