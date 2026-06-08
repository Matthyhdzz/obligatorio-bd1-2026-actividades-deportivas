DROP DATABASE IF EXISTS gestion_actividades_deportivas;
CREATE DATABASE gestion_actividades_deportivas;
USE gestion_actividades_deportivas;

CREATE TABLE facultades (
    id_facultad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    estado VARCHAR(20) NOT NULL
);

CREATE TABLE carreras (
    id_carrera INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_facultad INT NOT NULL,
    estado VARCHAR(20) NOT NULL,

    UNIQUE (nombre, id_facultad),

    FOREIGN KEY (id_facultad) REFERENCES facultades(id_facultad)
);

CREATE TABLE estudiantes (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    documento VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    id_carrera INT NOT NULL,
    estado VARCHAR(20) NOT NULL,

    FOREIGN KEY (id_carrera) REFERENCES carreras(id_carrera)
);

CREATE TABLE disciplinas (
    id_disciplina INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(255),
    estado VARCHAR(20) NOT NULL
);

CREATE TABLE espacios (
    id_espacio INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    ubicacion VARCHAR(150),
    capacidad INT,
    estado VARCHAR(20) NOT NULL
);

CREATE TABLE actividades (
    id_actividad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_disciplina INT NOT NULL,
    id_espacio INT NOT NULL,
    cupo_maximo INT NOT NULL,
    dia_semana VARCHAR(20) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    estado VARCHAR(20) NOT NULL,

    FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id_disciplina),
    FOREIGN KEY (id_espacio) REFERENCES espacios(id_espacio)
);

CREATE TABLE inscripciones (
    id_inscripcion INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    id_actividad INT NOT NULL,
    fecha_inscripcion DATE NOT NULL,
    estado VARCHAR(20) NOT NULL,

    UNIQUE (id_estudiante, id_actividad),

    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
    FOREIGN KEY (id_actividad) REFERENCES actividades(id_actividad)
);

CREATE TABLE asistencias (
    id_asistencia INT AUTO_INCREMENT PRIMARY KEY,
    id_inscripcion INT NOT NULL,
    fecha DATE NOT NULL,
    estado VARCHAR(20) NOT NULL,
    observacion VARCHAR(255),

    UNIQUE (id_inscripcion, fecha),

    FOREIGN KEY (id_inscripcion) REFERENCES inscripciones(id_inscripcion)
);