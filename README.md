# colonies
Automatic system for colony counter using DIP.
Sistema automático para conteo de colonias usando técnicas de DIP.

Proceso hasta ahora empleado:
1. Conversión a escala de grises.

1. Determinación de los centros de los pozos: por medio de correlación cruzada con un template circular de tono gris y hallando los mínimos locales de la matriz de correlación resultante que tuviesen distanciados por lo menos cierto número de pixeles.

2. Seccionamiento de los pozos: comprobando todos aquellos pixeles que se encontraran dentro de un círculo con un radio promedio especificado haciendo uso de los centros anteriormente obtenidos.

3. Segmentación: Primero se realiza una mejora de contraste y posteriormente se utiliza el método de Otsu para determinar un umbral adecuado el cual, luego se multiplica por el promedio de la imagen en escala de grises.


*----FALTA---*

4. Eliminación de las colonias que no cumplan con por lo menos 50 células: Uso de un filtro de tamaño.

5. Etiquetado y conteo: Se etiquetan las regiones que posean cierta conectividad y luego se realiza el conteo.
