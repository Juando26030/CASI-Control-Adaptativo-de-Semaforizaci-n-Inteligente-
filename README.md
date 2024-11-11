# CASI - Simulación de Semaforización Inteligente
<h2>Descripción</h2>
<p>Este proyecto es una simulación del <strong>Control Adaptativo de Semaforización Inteligente (CASI)</strong>, un sistema de semáforos interconectados diseñado para optimizar el flujo de tráfico en tiempo real en una ciudad. La simulación se enfoca en una red de 5 semáforos inteligentes, cada uno adaptándose de manera dinámica a las condiciones del tráfico en su intersección respectiva. CASI toma decisiones basadas en datos simulados que representan la cantidad de autos en espera en cada intersección, y ajusta los tiempos de los semáforos para maximizar la eficiencia del flujo vehicular.</p>

<h2>Objetivo</h2>
<p>El objetivo de esta simulación es <strong>representar visualmente el comportamiento de CASI</strong> y cómo optimiza el flujo de tráfico en una red de intersecciones mediante una visualización animada 2D. CASI simula datos que, en una implementación real, provendrían de sensores físicos en las intersecciones y datos abiertos de tráfico. En este proyecto, se utiliza <strong>programación orientada a objetos (POO)</strong> en Python para construir y organizar los componentes de la simulación.</p>

<h2>Características</h2>
<ul>
  <li><strong>Semáforos Inteligentes:</strong> Los semáforos cambian entre rojo, amarillo y verde, y ajustan sus tiempos de luz en función de la cantidad de autos esperando en cada intersección.</li>
  <li><strong>Detección de Tráfico:</strong> CASI simula datos de sensores que representan la cantidad de autos en espera, lo cual influye en la duración de los colores del semáforo.</li>
  <li><strong>Optimización Dinámica:</strong> El sistema CASI recopila datos de cada intersección y ajusta los semáforos para optimizar el flujo en tiempo real.</li>
  <li><strong>Visualización 2D:</strong> Utilizando pygame, se representa una visualización de autos y semáforos en una red de intersecciones para observar el comportamiento en tiempo real del sistema CASI.</li>
</ul>

<h2>Estructura del Proyecto</h2>
<p>El proyecto está organizado en varias <strong>clases principales</strong> que representan los componentes del sistema:</p>
<ul>
  <li><strong>Clase Semaforo:</strong> Representa un semáforo inteligente. Se adapta a las condiciones de tráfico en tiempo real, ajustando la duración de cada luz (rojo, amarillo, verde) según la cantidad de autos en espera.</li>
  <li><strong>Clase Auto:</strong> Representa un vehículo en movimiento. Cada auto verifica el estado de los semáforos y se detiene o avanza según el color de la luz en cada intersección.</li>
  <li><strong>Clase Intersección:</strong> Representa una intersección con un semáforo inteligente, controlando el flujo de autos que esperan o cruzan.</li>
  <li><strong>Clase ControladorCASI:</strong> El núcleo del sistema. Recopila datos de tráfico y ajusta los tiempos de los semáforos en cada intersección, optimizando el flujo general en base a las condiciones de tráfico simuladas.</li>
  <li><strong>Clase Simulación:</strong> Gestiona el ciclo de ejecución de la simulación, incluyendo la animación y visualización en tiempo real del tráfico.</li>
</ul>

<h2>Cómo Empezar</h2>

<h3>Prerrequisitos</h3>
<p>Para ejecutar esta simulación, necesitas tener instalado <strong>Python 3.8 o superior</strong> y los siguientes paquetes:</p>
<ul>
  <li><code>pygame</code> - Biblioteca para la visualización 2D en tiempo real.</li>
</ul>
<p>Para instalar pygame, ejecuta:</p>

<pre><code>pip install pygame</code></pre>

<h3>Ejecución de la Simulación</h3>
<ol>
  <li>Clona este repositorio:

    <pre><code>git clone https://github.com/Juando26030/CASI-Control-Adaptativo-de-Semaforizaci-n-Inteligente-.git</code></pre>
  </li>
  <li>Navega al directorio del proyecto:

    <pre><code>cd casi-semaforizacion-inteligente</code></pre>
  </li>
  <li>Ejecuta el archivo principal de la simulación:

    <pre><code>python main.py</code></pre>
  </li>
</ol>
<p>La simulación comenzará y se abrirá una ventana donde podrás observar el flujo de tráfico en las intersecciones y cómo <strong>CASI</strong> adapta los semáforos en tiempo real.</p>

<h2>Funcionamiento</h2>
<p>Cada semáforo en la simulación se adapta en función de los datos simulados de tráfico en su intersección respectiva. Estos datos determinan cuántos autos están esperando y, a partir de esta información, CASI ajusta la duración de cada color del semáforo para optimizar el flujo.</p>
<ul>
  <li><strong>Autos en Movimiento:</strong> Los autos avanzan y se detienen en cada intersección en función de los semáforos.</li>
  <li><strong>Optimización Dinámica:</strong> CASI recopila y procesa los datos de todas las intersecciones para lograr un flujo de tráfico más eficiente.</li>
</ul>

<h2>Futuras Mejoras</h2>
<p>Este proyecto es una versión simplificada de CASI, ideal para comprender y visualizar los conceptos básicos del sistema de semáforos inteligentes. Algunas posibles mejoras incluyen:</p>
<ul>
  <li>Ampliar el número de semáforos e intersecciones para una simulación más compleja.</li>
  <li>Implementar algoritmos más avanzados para optimización del tráfico.</li>
  <li>Integración con datos reales o simulados de sensores de tráfico para obtener una experiencia más realista.</li>
</ul>


