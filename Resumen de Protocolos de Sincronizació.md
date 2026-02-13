# Resumen de Protocolos de Sincronización en Redes Inalámbricas

## Protocolos Tradicionales

### 1. NTP (Network Time Protocol)
- Arquitectura jerárquica maestro–esclavo.
- Precisión aceptable en redes terrestres.
- Sensible a retrasos variables y poco adecuado para nodos con recursos limitados.

### 2. FTSP (Flooding Time Synchronization Protocol)
- Basado en difusión desde un nodo raíz.
- Buena precisión en redes de sensores.
- Vulnerable a cambios de topología y fallos de nodos.
- Genera sobrecarga de mensajes en escenarios grandes.

### 3. Protocolos Distribuidos (Consensus, WMTS, RLDS)
- No dependen de un nodo maestro.
- Cada nodo ajusta su reloj con base en vecinos.
- Más tolerantes a fallos, pero difíciles de mantener con alta precisión y bajo costo.
- Algunos requieren cálculos complejos (matrices, estimadores bayesianos).

### Limitaciones Comunes
- Diseñados para redes homogéneas (solo sensores, UAVs o satélites).
- Poca atención a interferencia dinámica (ruido, bloqueos, jamming).
- Sobrecarga de cómputo y comunicación.
- No se adaptan bien a pérdida total de enlaces satelitales.

---

## Protocolos Propuestos en el Artículo "A Novel Interference-Resilient Synchronization Framework for Space–Air–Ground Networks Using Neighbor-Aware Reinforcement Learning" publicado en IEEE INTERNET OF THINGS JOURNAL, VOL. 13, NO. 4, 15 FEBRUARY 2026

### NARL-MSS (Neighbor-Aware Reinforcement Learning – Master-Slave Synchronization)
- Se usa con **interferencia parcial** en enlaces satelitales.
- Nodo maestro (satélite) da referencia, esclavos se apoyan en vecinos si pierden conexión.
- Modelo de puntuación en línea para respuesta rápida.
- Aprendizaje por refuerzo para mejorar rendimiento a largo plazo.
- **Resultados:** 80% menos error de sincronización que protocolos clásicos.

### NARL-DS (Neighbor-Aware Reinforcement Learning – Distributed Synchronization)
- Se activa con **interferencia total** (todos los nodos pierden contacto con el satélite).
- Sincronización distribuida entre nodos vecinos.
- RL selecciona dinámicamente los mejores enlaces para minimizar costo y maximizar precisión.
- **Resultados:** Convergencia estable y reducción significativa de costos de sincronización.

---

## Conclusión
Los protocolos tradicionales funcionan bien en condiciones controladas, pero fallan frente a interferencia dinámica y en redes heterogéneas espacio–aire–tierra.  
El marco **NARL** propuesto en el artículo introduce un enfoque **adaptativo, ligero y resiliente**, capaz de alternar entre modos maestro–esclavo y distribuido según el nivel de interferencia.  
Esto permite mantener la precisión de los relojes internos (RTC) y reducir la sobrecarga de comunicación, incluso en escenarios extremos con pérdida parcial o total de enlaces satelitales.
