# colonies
Automatic system for colony counter using DIP.
Sistema automático para conteo de colonias usando técnicas de DIP.

Proceso hasta ahora empleado:

1. Conversión a escala de grises.

2. Mejora de contraste lineal.

3. Determinación de los centros de los pozos.
  3.1. Detección de bordes por método de Canny.
  3.2. Dilatación con elemento estructurante tipo diamante para definir mejor las formas circulares del recipiente de las cajas de Petri.
  3.3. Correlación cruzada con plantillas circulares binarias generadas.
  3.4. Encontrar los centros de los pozos por ubicación por medio del radio del pozo.

4. Seccionamiento de los pozos: comprobando todos aquellos pixeles que se encontraran dentro de un círculo con un radio promedio especificado haciendo uso de los centros anteriormente obtenidos.

5. Umbralización: mediante el método de Otsu se determina un umbral el cuál se escala por un factor igual al promedio de la imagen con el cual se umbraliza la imagen.

6. Segmentación de las colonias de los bordes por distancia euclidiana en el espacio de color CIE L*a*b.

7. Eliminación de las colonias que no tengan más de 50 células haciendo uso de propiedades geométricas de las regiones.

8 Etiquetado y conteo: Se etiquetan las regiones que posean cierta conectividad y luego se realiza el conteo.
