<img width="3087" height="469" alt="screenshot-2026-08-13_15-03-01" src="https://github.com/user-attachments/assets/39cf3913-7ef4-4ff3-9ae6-d00919543c77" />

<img width="1351" height="745" alt="screenshot-2026-08-13_15-03-53" src="https://github.com/user-attachments/assets/a4e76179-c1dc-47be-ac84-424c9141d2ca" />

<img width="1356" height="969" alt="screenshot-2026-08-13_15-04-13" src="https://github.com/user-attachments/assets/eb95e7a5-fccd-4e52-9982-f2637e6950f8" />

<img width="1839" height="1291" alt="screenshot-2026-08-13_15-04-29" src="https://github.com/user-attachments/assets/dc0a3d0d-82c7-4962-b638-f16b9f26d232" />

La call: cuanto mas alto esta el precio del subyacente respecto al strike, mas vale el derecho a comprarlo barato — y crece cada vez mas rapido a medida que se aleja del strike hacia arriba (curvatura convexa = lo que mide la griega gamma).

La put: Cuanto mas sube el subyacente, menos vale el derecho a venderlo a un precio fijo — se acerca a cero pero nunca es negativa (una opción nunca vale menos que $0, por eso se aplana en vez de seguir cayendo).


<img width="1686" height="1311" alt="screenshot-2026-08-13_15-04-46" src="https://github.com/user-attachments/assets/12e7328b-8ecb-40e7-b075-e0f25c73fb2e" />

Esto es un test de recuperacion, el notebook genero precios de opciones usando una volatilidad "real" conocida (eje X), despues uso Newton-Raphson para adivinar que volatilidad explica ese precio (eje Y), y comparo contra la linea identidad (y = x, la linea perfecta donde "lo que meti" = "lo que recupere").


<img width="1675" height="1380" alt="screenshot-2026-08-13_15-05-04" src="https://github.com/user-attachments/assets/f4a433a8-0244-442e-8223-6cc674f02122" />


A medida que ves hacia atras en el eje de volatilidad (de 0.0 a 0.8), el precio de la call sube, sin importar en que spot se encuentre. Eso es vega positiva, es decir, mas incertidumbre sobre hacia donde va el precio del subyacente = mas vale el derecho a comprarlo a precio fijo, porque tenes más upside potencial (y en una call, tu downside esta limitado a lo que pagaste — no hay simetria de riesgo). Se puede ver tambien que el crecimiento no es lineal, la superficie se "curva" más pronunciadamente hacia spots altos y volatilidades altas — ahí es donde gamma y vega interactuan mas fuerte.


<img width="1737" height="666" alt="screenshot-2026-08-13_15-05-25" src="https://github.com/user-attachments/assets/0aebc9c4-3839-4fec-bf12-e5e3e3839386" />
