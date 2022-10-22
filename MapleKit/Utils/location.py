"""
# -*- coding:utf-8 -*-
@Project : SmartKartRider
@File : LocateAll.py
@Author : Johan
@Time : 10/22/2022 12:59 PM

"""
import sys
import collections
import time
from mouseinfo import screenshot

try:
    import cv2, numpy
    useOpenCV = True
    RUNNING_CV_2 = cv2.__version__[0] < '3'
except ImportError:
    useOpenCV = False

RUNNING_PYTHON_2 = sys.version_info[0] == 2
if useOpenCV:
    if RUNNING_CV_2:
        LOAD_COLOR = cv2.CV_LOAD_IMAGE_COLOR
        LOAD_GRAYSCALE = cv2.CV_LOAD_IMAGE_GRAYSCALE
    else:
        LOAD_COLOR = cv2.IMREAD_COLOR
        LOAD_GRAYSCALE = cv2.IMREAD_GRAYSCALE

if not RUNNING_PYTHON_2:
    unicode = str # On Python 3, all the isinstance(spam, (str, unicode)) calls will work the same as Python 2.

GRAYSCALE_DEFAULT = False
USE_IMAGE_NOT_FOUND_EXCEPTION = False

class PyScreezeException(Exception):
    pass # This is a generic exception class raised when a PyScreeze-related error happens.

class ImageNotFoundException(PyScreezeException):
    pass # This is an exception class raised when the locate functions fail to locate an image.

Box = collections.namedtuple('Box', 'left top width height')
Point = collections.namedtuple('Point', 'x y')


def _load_cv2(img, grayscale=None):
    """
    TODO
    """
    # load images if given filename, or convert as needed to opencv
    # Alpha layer just causes failures at this point, so flatten to RGB.
    # RGBA: load with -1 * cv2.CV_LOAD_IMAGE_COLOR to preserve alpha
    # to matchTemplate, need template and image to be the same wrt having alpha

    if grayscale is None:
        grayscale = GRAYSCALE_DEFAULT
    if isinstance(img, (str, unicode)):
        # The function imread loads an image from the specified file and
        # returns it. If the image cannot be read (because of missing
        # file, improper permissions, unsupported or invalid format),
        # the function returns an empty matrix
        # http://docs.opencv.org/3.0-beta/modules/imgcodecs/doc/reading_and_writing_images.html
        if grayscale:
            img_cv = cv2.imread(img, LOAD_GRAYSCALE)
        else:
            img_cv = cv2.imread(img, LOAD_COLOR)
        if img_cv is None:
            raise IOError("Failed to read %s because file is missing, "
                          "has improper permissions, or is an "
                          "unsupported or invalid format" % img)
    elif isinstance(img, numpy.ndarray):
        # don't try to convert an already-gray image to gray
        if grayscale and len(img.shape) == 3:  # and img.shape[2] == 3:
            img_cv = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            img_cv = img
    elif hasattr(img, 'convert'):
        # assume its a PIL.Image, convert to cv format
        img_array = numpy.array(img.convert('RGB'))
        img_cv = img_array[:, :, ::-1].copy()  # -1 does RGB -> BGR
        if grayscale:
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    else:
        raise TypeError('expected an image filename, OpenCV numpy array, or PIL image')
    return img_cv



def _locateAll_opencv(needleImage, haystackImage, grayscale=None, limit=10000, region=None, step=1,
                      confidence=0.999):
    """
    TODO - rewrite this
        faster but more memory-intensive than pure python
        step 2 skips every other row and column = ~3x faster but prone to miss;
            to compensate, the algorithm automatically reduces the confidence
            threshold by 5% (which helps but will not avoid all misses).
        limitations:
          - OpenCV 3.x & python 3.x not tested
          - RGBA images are treated as RBG (ignores alpha channel)
    """
    if grayscale is None:
        grayscale = GRAYSCALE_DEFAULT

    confidence = float(confidence)

    needleImage = _load_cv2(needleImage, grayscale)
    needleHeight, needleWidth = needleImage.shape[:2]
    haystackImage = _load_cv2(haystackImage, grayscale)

    if region:
        haystackImage = haystackImage[region[1]:region[1]+region[3],
                                      region[0]:region[0]+region[2]]
    else:
        region = (0, 0)  # full image; these values used in the yield statement
    if (haystackImage.shape[0] < needleImage.shape[0] or
        haystackImage.shape[1] < needleImage.shape[1]):
        # avoid semi-cryptic OpenCV error below if bad size
        raise ValueError('needle dimension(s) exceed the haystack image or region dimensions')

    if step == 2:
        confidence *= 0.95
        needleImage = needleImage[::step, ::step]
        haystackImage = haystackImage[::step, ::step]
    else:
        step = 1

    # get all matches at once, credit: https://stackoverflow.com/questions/7670112/finding-a-subimage-inside-a-numpy-image/9253805#9253805
    result = cv2.matchTemplate(haystackImage, needleImage, cv2.TM_CCOEFF_NORMED)
    match_indices = numpy.arange(result.size)[(result > confidence).flatten()]
    matches = numpy.unravel_index(match_indices[:limit], result.shape)

    if len(matches[0]) == 0:
        if USE_IMAGE_NOT_FOUND_EXCEPTION:
            raise ImageNotFoundException('Could not locate the image (highest confidence = %.3f)' % result.max())
        else:
            return

    # use a generator for API consistency:
    matchx = matches[1] * step + region[0]  # vectorized
    matchy = matches[0] * step + region[1]
    for x, y in zip(matchx, matchy):
        yield Box(x, y, needleWidth, needleHeight)

def locate(needleImage, haystackImage, **kwargs):
    """
    TODO
    """
    # Note: The gymnastics in this function is because we want to make sure to exhaust the iterator so that the needle and haystack files are closed in locateAll.
    kwargs['limit'] = 1
    points = tuple(locateAll(needleImage, haystackImage, **kwargs))
    if len(points) > 0:
        return points[0]
    else:
        if USE_IMAGE_NOT_FOUND_EXCEPTION:
            raise ImageNotFoundException('Could not locate the image.')
        else:
            return None

def center(coords):
    """
    Returns a `Point` object with the x and y set to an integer determined by the format of `coords`.

    The `coords` argument is a 4-integer tuple of (left, top, width, height).

    For example:

    >>> center((10, 10, 6, 8))
    Point(x=13, y=14)
    >>> center((10, 10, 7, 9))
    Point(x=13, y=14)
    >>> center((10, 10, 8, 10))
    Point(x=14, y=15)
    """

    # TODO - one day, add code to handle a Box namedtuple.
    return Point(coords[0] + int(coords[2] / 2), coords[1] + int(coords[3] / 2))

def locateOnPicture(image, picture = 0, minSearchTime=0, **kwargs):
    """TODO - rewrite this
    minSearchTime - amount of time in seconds to repeat taking
    screenshots and trying to locate a match.  The default of 0 performs
    a single search.
    """
    start = time.time()
    while True:
        try:
            if type(picture) == "int":
                screenshotIm = screenshot(region=None) # the locateAll() function must handle cropping to return accurate coordinates, so don't pass a region here.
            else:
                screenshotIm = picture
            retVal = locate(image, screenshotIm, **kwargs)
            try:
                screenshotIm.fp.close()
            except AttributeError:
                # Screenshots on Windows won't have an fp since they came from
                # ImageGrab, not a file. Screenshots on Linux will have fp set
                # to None since the file has been unlinked
                pass
            if retVal or time.time() - start > minSearchTime:
                return retVal
        except ImageNotFoundException:
            if time.time() - start > minSearchTime:
                if USE_IMAGE_NOT_FOUND_EXCEPTION:
                    raise
                else:
                    return None

def locateCenterOnPicture(image, picture = 0, **kwargs):
    """
    TODO
    """
    coords = locateOnPicture(image, picture, **kwargs)
    if coords is None:
        return None
    else:
        return center(coords)

if useOpenCV:
    locateAll = _locateAll_opencv
    if not RUNNING_PYTHON_2 and cv2.__version__ < '3':
        NotImplemented
else:
    NotImplemented

if __name__ == "__main__":
    im = cv2.imread('D:/GameProjects/Kartrider/SmartKartRider/screenshot.png')
    image = cv2.imread("D:/GameProjects/Kartrider/SmartKartRider/raw_data/US/Button/Close-Window.PNG")
    retVal = locateCenterOnPicture(image, im)
    print(retVal)
    retVal = locateOnPicture(image, im)
    print(retVal)