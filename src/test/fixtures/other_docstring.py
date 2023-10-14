def find(pred, it, default=None):
    """Lorem ipsum dolor sit, amet consectetur adipisicing elit. Dicta quos quasi corrupti facilis nemo magni ipsa sit,
    quas culpa mollitia aut dolores fugiat obcaecati deleniti asperiores, omnis, officiis enim. Ullam.

    :param pred: Element -> bool - returns true when we find the value
    :param it: Iterable<Element> - the iterable to check through
    :param default: Element? - default value
    """
    return next((e for e in it if pred(e)), default)
