insert into public.transactions (
  category_id,
  amount,
  description,
)
values (
  %s,
  %s,
  %s
)
returning id
;
