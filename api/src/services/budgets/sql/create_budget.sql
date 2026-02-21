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
