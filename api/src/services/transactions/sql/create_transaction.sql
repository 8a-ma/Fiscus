insert into public.transactions (
  category_id,
  monto,
  descripcion,
)
values (
  %s,
  %s,
  %s
)
returning id
;
