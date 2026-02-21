update public.budgets
set
  deleted_at = (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
where
  id = %s
;
