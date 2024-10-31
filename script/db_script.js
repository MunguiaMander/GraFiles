mongosh
use grafiles_db; 

db.createCollection("users");
/*
    *Atributos
        - id
        - name
        - username
        - password
        - rol
*/

db.createCollection("files");
/*
    *Atributos
        - id
        - name
        - type
        - path
        - user
        - fecha_creacion
        - content
*/

db.createCollection("shared");
/*
    *Atributos
        - id
        - name
        - type
        - path
        - user_shared
        - content
        - fecha_compartido
        - hora_compartido
        - user
*/

db.createCollection("thrashed");
/*
    *Atributos
        - id
        - name
        - type
        - path
        - user
        - content
        - tipo_eliminacion
*/
