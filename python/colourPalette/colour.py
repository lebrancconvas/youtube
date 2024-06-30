from numpy import array
from sklearn.cluster import KMeans


class ColourGeneration():

    def generate(self, image, colourIndex):
        colourArray = array(image)
        reshape = colourArray.reshape(-1, 3)
        kmeans = KMeans(n_clusters=colourIndex)
        kmeans.fit(reshape)
        colours = kmeans.cluster_centers_
        colours = colours.astype(int)
        return colours


if __name__ == "__main__":
    ColourGeneration()
