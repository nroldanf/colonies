# colonies
Automatic system for colony counter using DIP.
Sistema automático para conteo de colonias usando técnicas de DIP.

Proceso hasta ahora empleado:

1. Determinación de los centros de los pozos: por medio de correlación cruzada con un template circular de tono gris y hallando los mínimos locales de la matriz de correlación resultante que tuviesen distanciados por lo menos cierto número de pixeles.
2. Seccionamiento de los pozos: comprobando todos aquellos pixeles que se encontraran dentro de un círculo con un radio promedio especificado haciendo uso de los centros anteriormente obtenidos.
3. 
