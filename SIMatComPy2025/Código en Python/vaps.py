import numpy as np

def vaps(M):
    MM = np.array(M)
    vp = np.linalg.eigvals(MM)
    return vp

# Ejemplo de uso
M = [[1, 5], [-1, -2]]
valores_propios = vaps(M)
print("Los valores propios son:", valores_propios)
