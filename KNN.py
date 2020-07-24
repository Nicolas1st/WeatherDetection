import cv2
import numpy as np
from statistics import mode


def get_histogram(segment):
    # to get histogram for every color
    bgr_planes = cv2.split(segment)

    blue_hist = cv2.calcHist(bgr_planes, channels=[0], mask=None, histSize=[16], ranges=[0, 256], accumulate=False)
    green_hist = cv2.calcHist(bgr_planes, channels=[1], mask=None, histSize=[16], ranges=[0, 256], accumulate=False)
    red_hist = cv2.calcHist(bgr_planes, channels=[2], mask=None, histSize=[16], ranges=[0, 256], accumulate=False)

    histogram = np.concatenate([blue_hist, green_hist, red_hist])

    return histogram


def compare_histograms(hist1, hist2):
    return cv2.compareHist(hist1, hist2, method=0)


def knn(point, compare_to, k=5):
    """
    other points - list of lists each containing:
    the coordinates - first
    the label - last
    """

    distances = []

    for other_point in compare_to:
        # because the -1 element is a label]
        print(type(other_point))
        other_point, label = other_point
        distance = cv2.compareHist(point, other_point, method=0)
        distances.append((distance, label))

    by_similarity = sorted(distances, key=lambda x: x[0], reverse=True)
    labels = [x[1] for x in by_similarity[:k]]

    return mode(labels)
