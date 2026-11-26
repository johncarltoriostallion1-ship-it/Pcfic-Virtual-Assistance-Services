-- Run once in Supabase -> SQL Editor -> Run
-- Lets the website READ settings/services, and signed-in users reach the tables
-- (row level security still decides who can actually change anything: only admins).
grant usage on schema public to anon, authenticated;
grant select on public.settings, public.services to anon, authenticated;
grant insert, update, delete on public.settings, public.services to authenticated;
grant execute on function public.is_admin() to anon, authenticated;
