-- db/init.sql

-- 1. Tabla de Usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla de Categorías
-- El CHECK asegura que el tipo sea solo uno de los permitidos
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('Gasto', 'Inversión', 'Fondo')),
    es_acumulativa BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabla de Presupuestos (Budgets)
-- Define cuánto planeas asignar a una categoría en un mes/año específico
CREATE TABLE IF NOT EXISTS budgets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
    mes INTEGER NOT NULL CHECK (mes BETWEEN 1 AND 12),
    anio INTEGER NOT NULL,
    monto_asignado DECIMAL(15, 2) DEFAULT 0.00,
    UNIQUE (user_id, category_id, mes, anio) -- Evita duplicados para el mismo mes/cat
);

-- 4. Tabla de Transacciones (La realidad)
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    monto DECIMAL(15, 2) NOT NULL,
    fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tabla de Balances Mensuales (MonthlyBalances)
-- Histórico para el sistema de "Sinking Funds" (Acumulados)
CREATE TABLE IF NOT EXISTS monthly_balances (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
    mes INTEGER NOT NULL CHECK (mes BETWEEN 1 AND 12),
    anio INTEGER NOT NULL,
    saldo_inicial DECIMAL(15, 2) DEFAULT 0.00, -- Lo que sobró del mes anterior
    saldo_final DECIMAL(15, 2) DEFAULT 0.00,   -- (Inicial + Presupuesto - Gastos)
    UNIQUE (category_id, mes, anio)
);
