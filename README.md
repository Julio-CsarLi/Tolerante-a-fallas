Funcionamiento del programa Demonio

1. El problema que deseas resolver
En muchos entornos (ya sea para seguridad personal, administración de servidores o automatización de flujos de trabajo), es crucial saber exactamente cuándo, cómo y qué archivos se están creando, modificando o eliminando dentro de un directorio específico.

2.Por qué requiere ejecución en segundo plano
Un monitor de carpetas está diseñado para ser un proceso continuo (24/7). Esto hace que la ejecución en segundo plano (como un demonio o servicio minimizado en la bandeja del sistema) sea un requisito no funcional 

No intrusividad: El usuario necesita seguir utilizando su computadora para otras tareas sin que una ventana de consola o interfaz gráfica ocupe espacio en la pantalla o en la barra de tareas.

Prevención de interrupciones: Al estar en segundo plano y ocultar la ventana principal en lugar de cerrarla, se evita que el usuario mate el proceso por accidente al hacer clic en la "X", garantizando la continuidad de la vigilancia.

3. Qué tipo de fallas podrían ocurrir
Los principales riesgos de falla son:

Bloqueos de archivos (File Locking): Que la aplicación intente registrar o leer un archivo que otro programa mantiene bloqueado por escritura exclusiva en ese mismo milisegundo.
Pérdida de la ruta vigilada: Que el usuario, o un proceso externo, mueva, renombre o elimine la carpeta raíz que el programa está vigilando, lo que causaría que el Observer arroje excepciones al intentar buscar una ruta inexistente.

4. Qué estrategia de tolerancia aplicarás
Para garantizar que el software sea robusto, se deben implementar las siguientes estrategias de tolerancia a fallos:

Manejo de Excepciones (Try/Except) localizados: Envolver las operaciones críticas (como la escritura en el archivo de log registro_eventos.txt) en bloques try...except. Si ocurre un error de permisos o de escritura, el programa debe capturar el error, registrarlo si es posible, y continuar funcionando en lugar de cerrarse abruptamente.

Validación de estado del demonio (Supervisión): Se puede implementar un patrón de "perro guardián" interno que verifique periódicamente si self.observer.is_alive() es True. Si el hilo muere por una falla imprevista, el sistema puede intentar reiniciarlo automáticamente usando la última ruta conocida.

Si ocurre un error crítico e irrecuperable (como la eliminación de la carpeta que mencionábamos antes o falta de espacio en disco para el archivo .txt), el sistema debe detener el servicio de vigilancia de manera limpia (usando observer.stop() y observer.join()), notificar al usuario mediante una alerta visual en la interfaz, y volver al estado de espera, evitando un cierre total de la aplicación.
