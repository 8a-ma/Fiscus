insert into public.categories
  (
    name,
    type,
    is_cumulative
  )
values (
  %s,
  %s,
  %s
)
on conflict (name, type)
do update set
  is_cumulative = excluded.is_cumulative
returning id
;
