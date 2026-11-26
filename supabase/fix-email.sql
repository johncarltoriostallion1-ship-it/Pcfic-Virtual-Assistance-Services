-- Run once in Supabase -> SQL Editor -> Run
-- Fixes the admin email spelling: pcficvaservices@gmail.com (not pcificvaservices)
insert into public.admins (email) values ('pcficvaservices@gmail.com') on conflict do nothing;
delete from public.admins where email = 'pcificvaservices@gmail.com';
update public.settings set value = 'pcficvaservices@gmail.com', updated_at = now()
where key = 'email' and value = 'pcificvaservices@gmail.com';
