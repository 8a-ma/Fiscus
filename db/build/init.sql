-- db/init.sql

-- 1. Tabla de Categorías
-- Define los tipos de categorias a los que los gastos y presupuestos estan asignados
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL,
    is_cumulative BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    UNIQUE (name, type)
);

-- 2. Tabla de Presupuestos (Budgets)
-- Define cuánto se planeas asignar a una categoría
CREATE TABLE IF NOT EXISTS budgets (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
    amount DECIMAL(15, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    deleted_at TIMESTAMP
);

-- 3. Tabla de Transacciones (La realidad)
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    amount DECIMAL(15, 2) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
);

-- 4. Tabla de Balances
-- Histórico para el sistema de "Sinking Funds" (Acumulados)
CREATE TABLE IF NOT EXISTS monthly_balances (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
    'month' INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    'year' INTEGER NOT NULL,
    initial_balance DECIMAL(15, 2) DEFAULT 0.00, -- Capital con el que se inicia el mes
    budgeted_amount DECIMAL(15, 2) DEFAULT 0.00, -- Capital asignado para el mes de la cateogoria
    actual_spent DECIMAL(15, 2) DEFAULT 0.00, -- Suma de todas las transacciones del mes para la cateogoria
    final_balance DECIMAL(15, 2) DEFAULT 0.00,   -- (initial + budget - spent)
    created_at TIMESTAMP DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    updated_at TIMESTAMP DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    UNIQUE(category_id, 'month', 'year')
);


CREATE OR REPLACE FUNCTION close_month_and_open_next(p_month INTEGER, p_year INTEGER)
RETURNS VOID AS $$
DECLARE
  next_month INTEGER;
  next_year INTEGER;
BEGIN
  IF p_month = 12 THEN
    next_month := 1;
    next_year := p_year + 1;
  ELSE
    next_month := p_month + 1;
    next_year := p_year;
  END IF;
  INSERT INTO monthly_balances (
    category_id,
    'month',
    'year',
    budget_amount,
    actual_spent,
    final_balance
  )
  SELECT
    c.id,
    p_month,
    p_year,
    COALESCE(b.amout, 0) as budgeted,
    COALESCE(SUM(t.amount), 0) as spent,
    (COALESCE(mb.initial_balance, 0) + COALESCE(b.amount, 0) - COALESCE(SUM(t.amount), 0)) as final
  FROM categories c
  LEFT JOIN budgets b on c.id = b.category_id AND b.deleted_at IS NULL
  LEFT JOIN transactions t on c.id = t.category_id AND EXTRACT(MONTH FROM t.created_at) = p_month AND EXTRACT(YEAR FROM t.created_at) = p_year
  LEFT JOIN montly_balances md ON c.id = md.category_id and mb.'month' = p_month and mb.'year' = p_year
  GROUP BY
    c.id,
    b.amount,
    mb.initial_balance
  ON CONFLICT (category_id, 'month', 'year')
  DO UPDATE SET
    budgeted_amount = EXCLUDED.budgeted_amount,
    actual_spent = EXCLUDED.actual_spent,
    final_balance = EXCLUDED.final_balance,
    updated_at = (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
  ;
  INSERT INTO montly_balances (category_id, 'month', 'year', initial_balance)
  SELECT
    category_id,
    next_month,
    next_year,
    CASE
      -- WHEN c.id = 1 THEN final_balance
      WHEN c.is_cumulative THEN final_balance
      ELSE 0
    END
  FROM montly_balances md
  JOIN categories c on mb.category_id = c.id
  ON CONFLICT (category_id, 'month', 'year')
  DO UPDATE SET
    initial_balance = EXCLUDED.initial_balance,
    updated_at = (CURRENT_TIMESTAMP AT TIME ZONE 'UTC');
END;
$$ LANGUAGE plpgsql;
