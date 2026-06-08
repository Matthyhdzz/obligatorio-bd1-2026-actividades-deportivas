USE gestion_actividades_deportivas;

INSERT INTO facultades (nombre, estado) VALUES
('Facultad de Ingeniería y Tecnologías', 'activa'),
('Facultad de Ciencias Empresariales', 'activa'),
('Facultad de Ciencias Humanas', 'activa'),
('Facultad de Ciencias de la Salud', 'activa');

INSERT INTO carreras (nombre, id_facultad, estado) VALUES
('Ingeniería en Informática', 1, 'activa'),
('Ingeniería Industrial', 1, 'activa'),
('Licenciatura en Sistemas', 1, 'activa'),
('Contador Público', 2, 'activa'),
('Administración de Empresas', 2, 'activa'),
('Psicología', 3, 'activa'),
('Comunicación', 3, 'activa'),
('Nutrición', 4, 'activa');

INSERT INTO disciplinas (nombre, descripcion, estado) VALUES
('Fútbol', 'Disciplina deportiva grupal orientada a fútbol recreativo.', 'activa'),
('Básquetbol', 'Disciplina deportiva grupal orientada a básquetbol.', 'activa'),
('Atletismo', 'Actividades físicas vinculadas a carrera, resistencia y técnica.', 'activa'),
('Vóleibol', 'Disciplina deportiva grupal de vóleibol.', 'activa'),
('Yoga', 'Actividad física orientada a flexibilidad, respiración y bienestar.', 'activa'),
('Funcional', 'Entrenamiento físico general por circuitos.', 'activa'),
('Gimnasio', 'Actividad de entrenamiento físico en sala de musculación.', 'activa');

INSERT INTO espacios (nombre, ubicacion, capacidad, estado) VALUES
('Cancha principal', 'Sector deportivo exterior', 30, 'activo'),
('Gimnasio universitario', 'Edificio central', 40, 'activo'),
('Sala multiuso', 'Bloque B', 20, 'activo'),
('Pista de atletismo', 'Sector deportivo exterior', 25, 'activo'),
('Cancha techada', 'Sector deportivo interior', 24, 'activo');

INSERT INTO actividades (
    nombre,
    id_disciplina,
    id_espacio,
    cupo_maximo,
    dia_semana,
    hora_inicio,
    hora_fin,
    estado
) VALUES
('Fútbol recreativo mixto', 1, 1, 10, 'Lunes', '18:00:00', '19:30:00', 'abierta'),
('Básquetbol inicial', 2, 5, 8, 'Martes', '17:30:00', '19:00:00', 'abierta'),
('Atletismo inicial', 3, 4, 12, 'Miércoles', '08:00:00', '09:30:00', 'abierta'),
('Vóleibol recreativo', 4, 5, 10, 'Jueves', '18:00:00', '19:30:00', 'abierta'),
('Yoga bienestar', 5, 3, 6, 'Viernes', '09:00:00', '10:00:00', 'abierta'),
('Funcional turno mañana', 6, 2, 5, 'Lunes', '07:30:00', '08:30:00', 'abierta'),
('Gimnasio libre supervisado', 7, 2, 15, 'Miércoles', '19:00:00', '20:30:00', 'cerrada');

INSERT INTO estudiantes (
    documento,
    nombre,
    apellido,
    correo,
    id_carrera,
    estado
) VALUES
('54123456', 'Matías', 'Hernández', 'matias.hernandez@correo.com', 1, 'activo'),
('51234567', 'Lucía', 'Pereira', 'lucia.pereira@correo.com', 1, 'activo'),
('49876543', 'Santiago', 'Rodríguez', 'santiago.rodriguez@correo.com', 2, 'activo'),
('52345678', 'Camila', 'Fernández', 'camila.fernandez@correo.com', 3, 'activo'),
('48765432', 'Agustín', 'Silva', 'agustin.silva@correo.com', 4, 'activo'),
('53456789', 'Valentina', 'Gómez', 'valentina.gomez@correo.com', 5, 'activo'),
('47654321', 'Federico', 'López', 'federico.lopez@correo.com', 6, 'activo'),
('54567890', 'Martina', 'Díaz', 'martina.diaz@correo.com', 7, 'activo'),
('46543210', 'Joaquín', 'Torres', 'joaquin.torres@correo.com', 8, 'activo'),
('55678901', 'Sofía', 'Martínez', 'sofia.martinez@correo.com', 1, 'activo');