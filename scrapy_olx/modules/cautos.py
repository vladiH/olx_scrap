
# coding: utf-8

# In[ ]:


class AutosOLX():
    def __init__(self, pMarca, pModelo, pAño, pKilometraje, pCondicion,
                 pCombustible, pColor, pTransmision, pTipoVendedor, pPrecio,
                 pLugar, pDiaPublicacion, pImage=""):
        self._marca = pMarca
        self._modelo =pModelo
        self._año =pAño
        self._kilometraje =pKilometraje
        self._condicion =pCondicion
        self._combustible =pCombustible
        self._color =pColor
        self._transmision =pTransmision
        self._tipoVendedor =pTipoVendedor
        self._precio =pPrecio
        self._lugar =pLugar
        self._diaPublicacion =pDiaPublicacion
        self._image = pImage

