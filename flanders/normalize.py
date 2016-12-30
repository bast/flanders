def normalize(v, s):
    """
    Normalize vector v to length s.
    """
    from math import sqrt

    length = sqrt(v[0]**2 + v[1]**2)

    return (s*v[0]/length, s*v[1]/length)
