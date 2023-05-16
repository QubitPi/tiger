import cv2
from image_similarity_measures.quality_metrics import metric_functions

def compare_two(img, base_img) -> dict:
    """
    Computes the similarity metrics of two given images.

    An example output is:

    {
        'fsim': nan,
        'issm': 0.0,
        'psnr': 36.294395682775026,
        'rmse': 0.0131818885,
        'sam': 89.86904735560465,
        'sre': inf,
        'ssim': 0.8884618469003556,
        'uiq': 0.037538160097775344
    }

    References:

    - https://pypi.org/project/image-similarity-measures/
    - https://betterprogramming.pub/how-to-measure-image-similarities-in-python-12f1cb2b7281
    - Collective metrics are defined in
      https://github.com/up42/image-similarity-measures/blob/master/image_similarity_measures/quality_metrics.py#L328

    :param img:  The image being compared
    :param base_img:  The image being compared to

    :return: a dictionary from string to obj
    """
    scale_percent = 100  # percent of original img size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    base_img = cv2.resize(base_img, dim, interpolation=cv2.INTER_AREA)

    return {metric: metric_function(img, base_img) for metric, metric_function in metric_functions.items()}
