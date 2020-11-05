# Entrega 5: Replicar casos 2-D para verificar
* Cambio de condiciones de borde:

  Para cambiar las condiciones de borde se debe considerar que los lados se representan de la siguiente forma:

  Borde izquierdo: u_k [0 , :]

  Borde derecho: u_k [-1 , :]

  Borde superior: u_k [: , -1]

  Borde inferior: u_k [: , 0]

  Entonces, para condiciones de borde con valores constantes simplemente se iguala la variable que corresponde al borde a la temperatura que se indica para cada caso, por ejemplo,
  si la condicion inicial para el borde izquierdo es de 20° grados, entonces se define de la siguiente forma:

  u_k [0 , :] = 20.

  Para los casos en que la condición de borde corresponde a un gradiente se considera la siguiente expresion:

  (f(x+h) - f(x) ) / dx = gradiente

  Lo que representado en el codigo se escribe de la siguiente forma:

  (borde x - borde x en paso de tiempo anterior) dividido en dx = gradiente

  Asi, si el borde derecho tiene como condicion inicial un gradiente de 20°, como codigo esto se ve como:

  (u_k [-1 , :] - u_k [-2 , :])/dx = -20.

  Finalmente se despeja el borde derecho que se definió en un principio:

  u_k [-1 , :] = 20. * dx + u_k [-2 , :]
