# Project 3

Web Programming with Python and JavaScript

Nombre: Enrique José Muñoz Avellán

Datos de ingreso para ver admin panel:
User: enrique
Password: 11111111

(8 veces 1)

Proyecto Pizza: Ordenando Deliciosas Pizzas en Línea
¡Bienvenido al proyecto Pizza! En este emocionante proyecto de CS50 Web, hemos creado una aplicación web utilizando el framework Django de Python para manejar las órdenes en línea de un restaurante de pizzas. Con esta aplicación, los usuarios pueden navegar por el menú del restaurante, agregar artículos a sus carritos de compras y confirmar sus órdenes. Por otro lado, los dueños del restaurante tienen la capacidad de gestionar los ítems del menú, ver las órdenes solicitadas y mucho más. A continuación, detallaremos las características clave de nuestra aplicación.

Requerimientos Implementados
1. Menú
Hemos asegurado que nuestra aplicación soporte todos los elementos del menú disponibles para Pinocchio's Pizza & Subs, un famoso lugar de pizzas en Cambridge. Para lograrlo, hemos construido modelos en Django que representan adecuadamente la información del menú. Estos modelos se encuentran en el archivo orders/models.py, y para garantizar que nuestra base de datos esté actualizada con estos modelos, hemos aplicado las migraciones correspondientes.

2. Agregar Items al Menú
Hemos utilizado Django Admin para proporcionar a los dueños del restaurante una interfaz sencilla y eficiente para agregar, actualizar y eliminar ítems del menú. Hemos agregado todos los ítems del menú de Pinocchio en nuestra base de datos, ya sea mediante el uso de la interfaz de administración o ejecutando comandos Python en el shell de Django.

3. Registro, Login, Logout
Los clientes pueden registrarse en nuestra aplicación web proporcionando su nombre de usuario, contraseña, primer nombre, apellido y dirección de correo electrónico. Implementamos un sistema de autenticación utilizando las tablas de autenticación predeterminadas de Django, lo que permite a los usuarios acceder y salir de la plataforma de manera segura y confiable.

4. Carrito de Compras
Una vez que los usuarios inician sesión, son recibidos con una representación visual del delicioso menú del restaurante. Aquí, pueden agregar elementos a su "carrito de compras" virtual. Hemos asegurado que el contenido del carrito se guarde incluso si el usuario cierra la ventana o se desconecta y vuelve a iniciar sesión más tarde.

5. Colocar una Orden
Una vez que el usuario tiene al menos un ítem en su carrito de compras, puede proceder a colocar una orden. Al hacerlo, se les presenta una alerta de confirmación para brindar una mejor experiencia de usuario.

6. Ver Órdenes
Los dueños del restaurante, como administradores del sitio, tienen acceso al admin panel de Django donde pueden visualizar todas las órdenes que los clientes han solicitado. Esto les proporciona una visión general de las transacciones y les permite gestionar el flujo de trabajo de manera efectiva.
Este es el apartado de "Sales" y "Sale Details".

7. Toque Personal
Nuestro toque personal en esta aplicación es la capacidad de los clientes para ver el estado de sus órdenes. Hemos incorporado un sistema de etiquetas (badges) que muestra si una orden está "pendiente" o "lista". Además, los administradores del negocio pueden cambiar el estado de una orden utilizando el Admin Panel de Django, lo que brinda un mayor control sobre el proceso de preparación de las pizzas.

Detalles Técnicos y Frontend
Hemos empleado el framework Django junto con el poderoso lenguaje de marcado HTML y el preprocesador de estilos CSS, Tailwind CSS, para crear una interfaz de usuario atractiva y altamente funcional. Para facilitar el desarrollo, hemos utilizado las librerías Daisy UI y HyperUI, que proporcionan componentes y estilos adicionales para mejorar la experiencia de usuario.

Nuestros modelos están cuidadosamente organizados y normalizados, lo que garantiza una lógica backend compleja pero sólida. La base de datos se encuentra bien estructurada para manejar eficientemente todos los datos relacionados con el menú, los usuarios y las órdenes.

Para mejorar la experiencia del usuario, hemos utilizado jQuery para implementar peticiones asíncronas al backend. Esto permite que los usuarios agreguen productos al carrito, realicen compras y actualicen el estado de sus órdenes sin necesidad de recargar la página.

Además, hemos incorporado la librería SweetAlert2 para mostrar alertas elegantes en la aplicación. Estas alertas mejoran la usabilidad y brindan una experiencia más agradable al interactuar con la plataforma.

¡Buen provecho y gracias por elegir nuestro servicio de pizzas en línea!
