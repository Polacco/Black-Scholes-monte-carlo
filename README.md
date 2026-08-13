# Black-Scholes & Monte Carlo Option Pricing

Implementacion desde cero de pricing de opciones europeas, validando el modelo 
analitico de Black-Scholes contra una simulacion de Monte Carlo del movimiento 
browniano geometrico — con verificación estadistica formal de la convergencia.

## Motivación

Este proyecto es el primer bloque de un programa personal de aprendizaje en 
finanzas cuantitativas. El objetivo no es solo calcular precios de opciones, 
sino **demostrar matematicamente** que dos metodos independientes (uno cerrado 
y exacto, otro probabilistico y simulado) convergen al mismo resultado, y que 
esa convergencia respeta la ley estadistica que la predice.

## Contenido

- **Pricing analitico de Black-Scholes**: formula cerrada para calls y puts 
  europeas, incluyendo las griegas (delta, gamma, vega, theta, rho).
- **Recuperacion de volatilidad implicita** via Newton-Raphson, validada 
  contra la linea de identidad.
- **Simulacion Monte Carlo** del proceso de movimiento browniano geometrico 
  (Euler-Maruyama), con pricing por promedio de payoffs descontados.
- **Validacion de convergencia**: verificacion empirica de que el error de 
  Monte Carlo decrece como 1/√n, con ajuste de pendiente en escala log-log.


## Estructura del proyecto
├── notebooks/ # Notebooks con las visualizaciones y el analisis
 ├── src/
 │ ├── black_scholes.py # Fórmulas analíticas, griegas, vol. implícita
 │ └── simulation.py # Simulación GBM y pricing Monte Carlo
 ├── tests/ # test_black_scholes.py
 └── requirements.txt


## Cómo correrlo

```bash
python -m venv venv
source venv/bin/activate  # en fish: source venv/bin/activate.fish
pip install -r requirements.txt
jupyter notebook notebooks/01_black_scholes_analytic.ipynb
```

Correr los tests:
```bash
pytest tests/ -v
```

## Resultados clave

### Ejemplo numerico basico

<img width="1351" height="745" alt="screenshot-2026-08-13_15-03-53" src="https://github.com/user-attachments/assets/a4e76179-c1dc-47be-ac84-424c9141d2ca" />

### Griegas principales
<img width="1356" height="969" alt="screenshot-2026-08-13_15-04-13" src="https://github.com/user-attachments/assets/eb95e7a5-fccd-4e52-9982-f2637e6950f8" />

### Precio de la call en funcion del spot

<img width="1839" height="1291" alt="screenshot-2026-08-13_15-04-29" src="https://github.com/user-attachments/assets/dc0a3d0d-82c7-4962-b638-f16b9f26d232" />

La call: cuanto mas alto esta el precio del subyacente respecto al strike, mas vale el derecho a comprarlo barato — y crece cada vez mas rapido a medida que se aleja del strike hacia arriba (curvatura convexa = lo que mide la griega gamma).

La put: Cuanto mas sube el subyacente, menos vale el derecho a venderlo a un precio fijo — se acerca a cero pero nunca es negativa (una opción nunca vale menos que $0, por eso se aplana en vez de seguir cayendo).


### Volatilidad implicita
<img width="1686" height="1311" alt="screenshot-2026-08-13_15-04-46" src="https://github.com/user-attachments/assets/12e7328b-8ecb-40e7-b075-e0f25c73fb2e" />

Esto es un test de recuperacion, el notebook genero precios de opciones usando una volatilidad "real" conocida (eje X), despues uso Newton-Raphson para adivinar que volatilidad explica ese precio (eje Y), y comparo contra la linea identidad (y = x, la linea perfecta donde "lo que meti" = "lo que recupere").

### Spot vs volatilidad

<img width="1675" height="1380" alt="screenshot-2026-08-13_15-05-04" src="https://github.com/user-attachments/assets/f4a433a8-0244-442e-8223-6cc674f02122" />


A medida que ves hacia atras en el eje de volatilidad (de 0.0 a 0.8), el precio de la call sube, sin importar en que spot se encuentre. Eso es vega positiva, es decir, mas incertidumbre sobre hacia donde va el precio del subyacente = mas vale el derecho a comprarlo a precio fijo, porque tenes más upside potencial (y en una call, tu downside esta limitado a lo que pagaste — no hay simetria de riesgo). Se puede ver tambien que el crecimiento no es lineal, la superficie se "curva" más pronunciadamente hacia spots altos y volatilidades altas — ahí es donde gamma y vega interactuan mas fuerte.


### Validacion Black-Scholes vs Monte Carlo

<img width="1737" height="666" alt="screenshot-2026-08-13_15-05-25" src="https://github.com/user-attachments/assets/0aebc9c4-3839-4fec-bf12-e5e3e3839386" />



**CONVERGENCIA DE MONTE CARLO**

<img width="3058" height="334" alt="screenshot-2026-08-13_15-47-13" src="https://github.com/user-attachments/assets/2cfd7339-042c-4a9a-b159-9edc732de794" />

### Simulacion de distintos numeros de trayectorias posibles


<img width="2574" height="1624" alt="screenshot-2026-08-13_15-47-38" src="https://github.com/user-attachments/assets/88139485-fce7-465b-ab72-d3d9da38103b" />

Lo importante de destacar de aqui es que para casi todos los n, los valores son muy parecidos entre si. Por ejemplo en n=100000, error real 0.0366 vs error teorico esperado 0.0465 (columnas means_abs_error y mean_se). Eso es una segunda confirmacion de lo anterior. O sea, no solo el error cae a la velocidad correcta, sino que su magnitud en cada punto es consistente con lo que predice la formula SE = σ/√n. 

Dos formas distintas de validar la misma ley, ambas cierran.


### Tabla de resultados

<img width="1729" height="844" alt="screenshot-2026-08-13_15-49-44" src="https://github.com/user-attachments/assets/0bb41ff8-748d-49e4-bb16-943643e7f294" />



**GRAFICO DE CONVERGENCIA**
<img width="2148" height="792" alt="screenshot-2026-08-13_15-50-18" src="https://github.com/user-attachments/assets/571e5c0e-a38f-4165-ba73-64fdbe044218" />

La curva de error real (azul) sigue casi perfectamente a la linea de referencia teorica 1/√n (negra punteada), junto con la linea verde del error estandar teorico que se encuentra practicamente pegada tambien. El único tramo donde "se despega" un poco es entre n=10 y n=100, que es exactamente donde se debe de esperar ruido, ya que con pocas trayectorias, la ley de los grandes numeros todavia no formo un promedio, asu que una corrida puntual puede dar un error mas alto o mas bajo de lo que predice la formula solo por "casualidad". A partir de n=500 en adelante, la curva se vuelve una recta limpia, que es el comportamiento asintotico que debe de tener segun la teoria.

El grafico de la derecha es lo mismo pero desde otro angulo. la banda de confianza (±1 SE) se va cerrando como un embudo a medida que crece n, y el precio Monte Carlo (linea azul) converge hacia la linea roja de Black-Scholes, quedando siempre dentro de la banda. Es la misma ley 1/√n pero visualizada como "certeza creciente" en vez de "error decreciente". Es lo mismo.


### Verificacion numerica de la pendiente

<img width="1236" height="541" alt="screenshot-2026-08-13_15-52-59" src="https://github.com/user-attachments/assets/c400154b-ba64-4f9e-87b0-22a78da2b171" />

Esta es la verdadera prueba de fuego. Esto es ajustar una regresion lineal sobre el grafico log-log (en escala log-log, y = C·n^(-0.5) se convierte en una recta con pendiente -0.5, porque log(y) = log(C) - 0.5·log(n)). Una diferencia de 0.011 sobre un valor esperado de -0.5 es un error del 2%, totalmente dentro de lo esperable dado que es una sola corrida de simulacion (no estamos promediando sobre varias semillas para cada n, asi que algo de ruido estadistico es normal).

Si se quiere una pendiente todavia mas ajustada a -0.500 exacto, la forma de lograrlo seria repetir cada n varias veces con distintas semillas y promediar el error.


### Autor 
_Joaquin M. Polacco_
