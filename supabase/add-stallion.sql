-- Run once in Supabase -> SQL Editor -> Run
-- Adds Stallion Graphics and Web Designs as a client (shown on the Clients page).
-- Logo: loaded from their own website for now. After the next GitHub upload you can switch it to
-- 'assets/img/clients/stallion.png' (or just upload a logo in Admin -> Clients -> Edit -> Replace logo).
insert into public.clients (slug, name, short_name, industry, location, about, website, services, logo_url, images, show_on_clients, sort_order)
select
  'stallion',
  'Stallion Graphics and Web Designs',
  'Stallion',
  'Graphic & Web Design',
  'Philippines',
  'A Filipino design studio creating logos, branding, booking sites, online stores and websites for growing businesses.',
  'https://stallion-website-omega.vercel.app',
  '{}'::text[],
  'https://stallion-website-omega.vercel.app/assets/img/logo-mark-320.png',
  '[]'::jsonb,
  true,
  coalesce((select max(sort_order) from public.clients), 0) + 10
where not exists (select 1 from public.clients where slug = 'stallion');
