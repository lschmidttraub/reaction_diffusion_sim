import numpy as np
import scipy.ndimage as ndi


def laplacien1D(a):
    """
    Calculer l'opérateur laplacien discrétisé d'un tableau à 1 dimension.

    Args:
        a (numpy.ndarray): tableau à 1 dimension

    Returns:
        numpy.ndarray: laplacien du tableau a
    """
    return (
        - 2 * a
        + np.roll(a, 1, axis=0)
        + np.roll(a, -1, axis=0)
    )


def laplacien2D(a):
    """
    Calculer l'opérateur laplacien d'un tableau à 2 dimensions.

    Args:
        a (numpy.ndarray): tableau à 2 dimensionS

    Returns:
        numpy.ndarray: laplacien du tableau a
    """
    return (
        - 4 * a
        + np.roll(a, 1, axis=0)
        + np.roll(a, -1, axis=0)
        + np.roll(a, +1, axis=1)
        + np.roll(a, -1, axis=1)
    )


def symetrique(a, symetrie):
    """
    Calcule un tableau qui est symétrique par rotation de degré 360/symetrie.

    Args:
        a (numpy.ndarray): tableau à 2 dimensions
        symetrie (int): nombre de degrés de symétrie

    Returns:
        np.array: tableau symétrique, moyenne des rotations de a
    """
    deg = 360/symetrie
    return np.mean([ndi.rotate(a, deg*i, reshape=False, mode="wrap") for i in range(symetrie)], axis=0)


def initialisation_aleatoire(forme, symetrie=0):
    """
    Générer deux tableaux aux valeurs aléatoires comprises entre 0 et 1.

    Args:
        forme ((int,int)): forme des tableaux
        symetrie (int): nombre de degrés de symétrie (0 si aucun)

    Returns:
        (np.array, np.array): 2 tableaux initialisés
    """
    a, b = (np.random.random(forme), np.random.random(forme))
    if symetrie:
        a, b = symetrique(a, symetrie), symetrique(b, symetrie)
    return a, b


def initialisation_GS(forme, symetrie=0):
    """
    Fonction d'initialisation du modèle Gray-Scott.

    Args:
        forme ((int,int)): forme des tableaux
        symetrie (int): nombre de degrés de symétrie (0 si aucun)

    Returns:
        (np.array, np.array): 2 tableaux initialisés
    """
    a = np.ones(forme)
    b = np.zeros(forme)
    if len(a.shape) == 1:
        centre = a.shape[0]//2
        a[centre-20:centre+20] = 0.5
        b[centre-20:centre+20] = 0.5
    else:
        centre_L = forme[0] // 2
        centre_l = forme[1] // 2

        a[centre_L-20:centre_L+20, centre_l-20:centre_l+20] = 0.5
        b[centre_L-20:centre_L+20, centre_l-20:centre_l+20] = 0.25

    a += np.random.normal(scale=0.05, size=forme)
    b += np.random.normal(scale=0.05, size=forme)
    if symetrie:
        a, b = symetrique(a, symetrie), symetrique(b, symetrie)
    return a, b


def initialisation_gaussienne(forme):
    """
    Générer deux tableau de dimension forme en choisissant des valeurs aléatoire parmis une distribution normale.

    Args:
        forme ((int,int)): forme des tableaux

    Returns:
        (numpy.ndarray, numpy.ndarray): deux tableaux intialisés
    """
    return np.random.normal(scale=0.05, size=forme), np.random.normal(scale=0.05, size=forme)


def perturbation(forme):
    """
    Crée une perturbation au centre d'un tableau rempli de 0

    Args:
        longueur (int): longueur des tableaux

    Returns:
        numpy.ndarray: tableaux initialisés
    """
    forme = np.array(forme)
    a = np.zeros(forme)
    if len(a.shape) == 1:
        a[a.shape[0] // 2] = 0.5
    elif len(a.shape) == 2:
        a[a.shape[0] // 2, a.shape[1] // 2] = 0.5
    return a, np.zeros(forme)
