-- db/init.sql

-- 1. Tabla de Categorías
-- Define los tipos de categorias a los que los gastos y presupuestos estan asignados
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL
    is_cumulative BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla de Presupuestos (Budgets)
-- Define cuánto se planeas asignar a una categoría en un mes/año específico
CREATE TABLE IF NOT EXISTS budgets (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
    amount DECIMAL(15, 2) DEFAULT 0.00,
    budget_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    UNIQUE (id, category_id)
);

-- 3. Tabla de Transacciones (La realidad)
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    monto DECIMAL(15, 2) NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabla de Balances Mensuales (MonthlyBalances)
-- Histórico para el sistema de "Sinking Funds" (Acumulados)
CREATE TABLE IF NOT EXISTS monthly_balances (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
    start_balance DECIMAL(15, 2) DEFAULT 0.00, -- Lo que sobró del mes anterior
    final_balance DECIMAL(15, 2) DEFAULT 0.00,   -- (Inicial + Presupuesto - Gastos)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    UNIQUE (id, category_id)
);
