update public.budgets
set
  deleted_at = (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
where
  %s
;

insert into public.budgets (
  category_id,
  amount,
)
values (
  %s,
  %s
)
returning id
;
