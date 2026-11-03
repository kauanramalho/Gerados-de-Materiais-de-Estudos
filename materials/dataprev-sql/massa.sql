PRAGMA foreign_keys = ON;
CREATE TABLE Aluno (id INTEGER PRIMARY KEY, nome TEXT NOT NULL, nota_maxima REAL);
CREATE TABLE Curso (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL);
CREATE TABLE Matricula (
 aluno_id INTEGER NOT NULL REFERENCES Aluno(id),
 curso_id INTEGER NOT NULL REFERENCES Curso(id),
 nota REAL, status TEXT NOT NULL,
 PRIMARY KEY (aluno_id, curso_id)
);
INSERT INTO Aluno VALUES (1,'Ana',99),(2,'Beto',99),(3,'Caio',99),(4,'Dora',99);
INSERT INTO Curso VALUES (10,'SQL'),(20,'Redes'),(30,'Linux');
INSERT INTO Matricula VALUES (1,10,8,'ativa'),(1,20,NULL,'cancelada'),(2,10,6,'ativa'),(3,20,NULL,'ativa');
