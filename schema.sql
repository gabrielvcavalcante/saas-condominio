CREATE TABLE IF NOT EXISTS condominios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    endereco VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    condominio_id INT,
    unidade VARCHAR(20) NOT NULL,
    pin VARCHAR(50) NOT NULL,
    perfil VARCHAR(20) NOT NULL,
    FOREIGN KEY (condominio_id) REFERENCES condominios(id)
);

CREATE TABLE IF NOT EXISTS chamados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    condominio_id INT,
    usuario_id INT,
    titulo VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'Pendente',
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (condominio_id) REFERENCES condominios(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);