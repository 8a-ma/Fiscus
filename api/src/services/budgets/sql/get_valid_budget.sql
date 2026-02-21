select
  id,
  category_id,
  amout,
  created_at
from
  public.budgets
where
  deleted_at = null
