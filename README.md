# Proyecto 2 - Hito 1 | Inverted Index

## Introducción

El análisis de textos se ha vuelto un tema altamente estudiado, pues los distintos métodos de análisis y de trabajo agilizan varios procesos. Entre estos, se encuentra la indexación de documentos, el cual tiene como fin reducir el tiempo de búsqueda de palabras y frases, así como también reducir el peso y el tamaño de los archivos utilizados. La indexación se basa en tomar las palabras clave de los documentos de una colección, con el fin de ayudar en las subsiguientes búsquedas. Hay varios tipos de indexación usadas sobre documentos, nosotros trabajando sobre el concepto de indice invertido. En este, luego de procesar las palabras clave, se saca la raiz de dicha palabra y se guarda el documento en el cual fue encontrado, asi como la frecuencia de apariciones, con el fin de poder trabajar con múltiples archivos y analizar efectivamente el texto en distintas formas.

## Marco Teórico
La elaboración de este proyecto se ha basado no en la implementación misma, si no en la utilidad que se le quiere dar al producto. Para ello, el uso del **Índice Invertido** resulta particularmente conveniente, pues nos permite llevar un conteo correcto de las palabras y los *tweets* en los que aparece. Dada la gran cantidad de *tweets* en general y por precauciones relacionadas a la cantidad de memoria principal, se decidió utilizar **SPIMI**, single-pass in-memory indexing, un método de organización para el Índice Invertido que consiste en armar índices para cada bloque, y no necesariamente mapear las palabras a su contraparte como identificador. En su lugar, dentro de cada bloque se tiene un índice para su información particular. Estos luego pueden mezclarse para hacer algo similar a un index más grande y completo, que a su vez tiene menos restricciones en cuanto al ordenamiento de los documentos que lo componen. 

Una parte importante tanto como del Índice invertido como del método de busqueda del que se hablará más adelante son el **Inverse Document Frequency** y el **Term Frequency**, también conocidos como **idf** y **tf** respectivamente. El *idf* es la frecuencia inversa con la que se encuentra un token específico en los documento de la colección o, dicho de otra forma, cuantos documentos de toda la colección contienen al token. Este dato es útil porque nos permite saber la relevancia de una palabra de acuerdo a su especificidad, pues el simple hecho que se mencione en pocos documentos significa que es una palabra más rara en la colección. El *tf*, por otro lado, viene a ser el número de veces en las que aparece un token específico en un documento específico. Este es útil de alguna forma por el motivo opuesto, pues nos indica que con mayor frecuencia de una palabra en un documeto específico, representa que tiene una gran importancia sobre únicamente ese documento. Estas dos, aunque son buenas métricas, tienen un mejor funcionamiento aún cuando se juntan en algo conocido como **tf-idf**, que multiplica el peso normalizado de tanto el *tf* y el *idf* de tal forma que ambas métricas del token queden representadas en un solo valor.

Para la búsqueda utilizamos el concepto de la **Distancia Coseno**, de esa manera pudiendo trabajar la similitud entre una query y la información de los *tweets* ya analizados. Esta nos permite hallar una distancia dependiente netamente de la similitud de sus terminos de acuerdo a sus pesos *tf-idf*, obteniendo la distancia euclediana de las componentes del vector y dividiendo esta por la **norma** de dicho documento, obteniendo el vector normalizado de los documentos comparados. Así, al multiplicar dichos resultados, podremos obtener un scoring para cada documento comparado con la query, ordenados por su similitud, los cuales serían luego presentados en la plataforma.

## Implementación & Resultados
En esta sección del texto, se mostrará la implementación en Python de un índice invertido con el fin de encontrar similitud de una frase con una base de datos de tweets.

### Construcción del índice invertido
Como paprte de nuestra implemntación, el Índice Invertido tuvo el siguiente formato:
```
InvertedIndex = { token : [ df , { docid : tf } ] }
```
Como se muestra expresado en forma de código, nuestro Índice Invertido es un diccionario que tiene por llave los tokens que hay en la página de memoria, y que tiene por valor un arreglo cuyo primer elemento es su **Document Frequency**, y cuyo segundo elemento es otro diccionario cuya llaves son los documentos que contienen a dicho token y cuyo valor sería la **Term Frequency** en ese documento. La utilidad de la implementación de esta estructura está en la reutilización de estos valores y su rápido acceso para el cálculo del **tf-idf**, siendo también necesario este diseño para la indexación en bloques que hablaremos más adelante. En el programa que se encuentra en el [Github](https://github.com/Mauricio-Bernuy/BD2-P2-H1) del proyecto, se puede ver como se accede directamente a los valores pre-calculados del índice para poder hacer algunos de estos cálculos, como por ejemplo el de la norma.

La construcción misma del índice invertido se basa en un proceso iterativo basado en bloques de memoria, el cual se discute en el siguiente punto. En la siguiente función, se ve la implementación que se utilizó.
![](https://i.imgur.com/3F2vgRh.jpg)



### Manejo en memoria secundaria 
Siguiendo el concepto de indexación por bloques y el **SPIMI**, los índices serán almacenados en archivos separados del tamaño de un bloque de memoria, con el fin de opimizar al máximo el intercambio de datos entre memoria principal y secundaria. Cada uno de estos índices contará con su propio diccionario, con sus propios **tf** y **df**, siendo construído por la función de build index hasta llegar a un tamaño maximo definido, momento en el cual será transferido a un archivo en memoria secundaria usando la librería **pickle**, y empezando a llenar otro bloque de memoria hasta que el índice se encuentre totalmente construído. 

El diseño de este índice permite que todos los archivos separados sean mezclados en un solo índice completo, idéntico al resultante del original, utilizando un método similar a un *mergesort*. Se utiliza un algoritmo para mezclar los incidencias de los tokens sumando sus *Document Frequencies*, y sus producciones se combinan asemejando a un OR. Este se repite hasta obtener el índice completo. En la siguiente imagen, se ve la iteración que se hace.

![](https://i.imgur.com/iP2GvYS.jpg)
![](https://i.imgur.com/esefaf7.jpg)


### Calcular similitudes
El cálculo de las distancias, como se mencionó previamente, está basado en la **Distancia Coseno**. Su implementación específica esta basada en hacer un análisis inicial de la query y luego comparar dicha query con todo el resto de documentos en el Índice Invertido principal. Por conveniencia en la programación y para poder reutilizar las funciones designadas al cálculo del *idf* y *tf*, se arma un pequeño Índice Invertido solamente para la query. El *df* del mismo se obtiene del Índice Invertido principal de los *tweets*, mientras el resto de información por termino se guarda en el mismo formato tal que es compatible y comparable directamente con cualquiera de los otros documentos. De esa forma se aplica directamente la fórmula:
![](https://i.imgur.com/WE5CNmh.png),
donde qi es el peso idf-tf del query para el término i, y di es el peso idf-tf del documento para el término i. Se usan las siguientes funciones para calcularlo:

![](https://i.imgur.com/sbr0IEy.jpg)

Estos son utilizados por lo tanto en la función de búsqueda:
![](https://i.imgur.com/RvR8rO9.jpg)

Los resultados son finalmente enlistados como un arreglo de pares (similitud, docid) ordenados por similitud de forma descendente, de forma que estos puedan ser accedidos cómodamente por la aplicación que los muestra.

### Aplicación
Con el fin de crear una aplicación y probar los métodos implementados, se utilizó **Flask** para realizar un backend compatible con Python, y se utilizó HTML con Bootstrap y Javascript para el frontend.

El programa para ejecutar Flask es el siguiente:
![](https://i.imgur.com/JzyfTgf.jpg)
Este hace uso de las funciones previamente implementadas, las carga y las comunica a sus archivos en html que reciben el arreglo de resultados y los muestra.

La aplicación se ve de la siguiente manera habiendo hecho una búsqueda de "hola", mostrando tanto el tweet como su relevancia asociada.
![](https://i.imgur.com/k5lCeus.png)


Lo primero que se hace es escoger los *tweets* recopilados, y luego de cargarlos, se debe ingresar el query, frase que va a ser buscada. Posteriormente, se presiona el boton de "Show Results", y este muestra los tweets, junto con su Scoring, del mas cercano al mas lejano.

## Conclusiones

En conclusión, podemos ver que el uso de índices invertidos agiliza la búsqueda de una frase similar dentro de un conjunto grande de textos. Esto se evidencia en los tiempos en los cuales se construye el índice, y en la presentación de los resultados. El método de Scoring utilizado enfatiza la eficiencia del sistema y logramos presentar los valores en corto tiempo.

Para un futuro trabajo, consideramos que sería mejor planear el manejo de los archivos, pues tuvimos problemas accediendo a las carpetas en el frontend para mostrar los resultados.
