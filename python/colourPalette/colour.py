from numpy import array, reshape
from sklearn.cluster import KMeans


class ColourGeneration():
    def generateColours(self, image, rangeVal):
        colourArray = array(image)
        reshape = colourArray.reshape(-1, 3)
        kmeans = KMeans(n_clusters=rangeVal)
        kmeans.fit(reshape)
        colours = kmeans.cluster_centers_
        colours = colours.astype(int)
        return colours

if __name__ == "__main__":
    ColourGeneration()


