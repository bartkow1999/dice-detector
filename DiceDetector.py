import cv2
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy
import pathlib


def blobDetectorParameters():
    '''
    All parameters needed to blob detector object to work properly
    '''
    # blob detector parameter object
    params = cv2.SimpleBlobDetector_Params()

    # thresholding min->max
    params.minThreshold = 30
    params.maxThreshold = 200

    # minArea < blobArea < maxArea
    params.filterByArea = True
    params.minArea = 40
    params.maxArea = 1000

    # 0 <= blob circularity <= 1
    params.filterByCircularity = True
    params.minCircularity = 0.4

    # 0 <= blob inertia ratio <= 1
    params.filterByInertia = True
    params.minInertiaRatio = 0.4

    return params


def blobDetector(params):
    '''
    Takes parameters from blobDetectorParameters() function and performs the creation of blob detector object
    '''
    # blob detector object
    detector = cv2.SimpleBlobDetector_create(params)
    return detector


def img_keypoints(detector, img):
    '''
    Detects all blob-like points on the picture
    '''
    img_keypoints = detector.detect(img)

    # detects blobs on inverted picture (dices can have different color schemes)
    inv_img = cv2.bitwise_not(img)
    img_keypoints_inv = detector.detect(inv_img)

    # combines blobs on normal and inverted picture
    all_keypoints = img_keypoints + img_keypoints_inv

    return all_keypoints


def clusterParameters(keypoints):
    '''
    All parameters needed to clustering function to work properly
    '''
    distance = 50
    coords = np.array([list(keypoint.pt) for keypoint in keypoints])
    text_position = (36, 36)
    fontsize = 32
    color = 'red'

    # if there is no blobs on picture, it returns the -1 value
    if len(coords) > 0:
        return (coords, distance, text_position, fontsize, color)
    else:
        return -1


def clusters_plus_plot(params):
    '''
    Performs the cluster function, which main aim is to connect blobs close to each others and treats it
    as a group/entity
    '''
    clusters = scipy.cluster.hierarchy.fclusterdata(params[0], params[1], criterion='distance')

    # Detects clusters
    cluser_centers = []
    for cluster_pieces in np.unique(clusters):
        cluser_centers.append(
            (np.sum(clusters == cluster_pieces), [params[0][np.where(np.array(clusters) == cluster_pieces)[0]]]))

    # print the number of pieces for every cluster
    for cluster_pieces, cluster_data in cluser_centers:
        plt.text(cluster_data[0][0][0] + params[2][0], cluster_data[0][0][1] + params[2][1], s=str(cluster_pieces),
                 fontsize=params[3], color=params[4])


def plotting_basic(img, all_keypoints):
    '''
    Makes the basic plot with original image and keypoints detected by the blob detector
    '''
    # area for plot
    plt.figure(figsize=(24, 24))
    # switches of x and y axes
    plt.axis('off')
    # shows the original picture with drawn keypoints
    plt.imshow(img)
    drew_keypoints = cv2.drawKeypoints(img, all_keypoints, np.array([]), (0, 0, 255),
                                       cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    plt.imshow(cv2.cvtColor(drew_keypoints, cv2.COLOR_BGR2RGB))


def superposition(img):
    '''
    This function is a connector between all subfunctions in the dice detector project.
    '''
    detector_parameters = blobDetectorParameters()
    blob_detector = blobDetector(detector_parameters)
    detected_blob_points = img_keypoints(blob_detector, img)
    plotting_basic(img, detected_blob_points)

    cluster_parameters = clusterParameters(detected_blob_points)
    # if there is no blobs on picture, skip clustering function
    if cluster_parameters != -1:
        clusters_plus_plot(cluster_parameters)

    # showing the result of the program
    plt.show()


def main():
    '''
    This is the main() function, which manages a few operations:
    -> reads dice pictures by the program (resources/dices/ + subfolder)
    -> performs superposition() function
    '''
    folder_path = 'resources/dices/'
    subfolders = ['dices_all/']  # ['dices_easy', 'dices_medium', 'dices_hard', 'dices_extra_hard']
    for subfolder in subfolders:
        for file in pathlib.Path(folder_path + subfolder).iterdir():
            img = cv2.imread(str(file))
            superposition(img)
            break # only the first picture


if __name__ == "__main__":
    main()
