-- =====================================================================
-- PCFIC website admin: run this once in Supabase -> SQL Editor -> Run
-- Safe to run again (it will not duplicate data).
-- =====================================================================

-- 1) Who is allowed to edit (only emails in this list can save changes)
create table if not exists public.admins (
  email text primary key
);
insert into public.admins (email) values ('pcficvaservices@gmail.com')
on conflict do nothing;
alter table public.admins enable row level security;   -- no policies: not readable from the website

create or replace function public.is_admin()
returns boolean
language sql stable security definer set search_path = public
as $$
  select exists (
    select 1 from public.admins
    where lower(email) = lower(coalesce(auth.jwt() ->> 'email', ''))
  );
$$;

-- 2) Simple site settings (logo, contact details, home headline)
create table if not exists public.settings (
  key        text primary key,
  value      text not null default '',
  updated_at timestamptz not null default now()
);

insert into public.settings (key, value) values
  ('logo_url',         ''),
  ('hero_line1',       'Clean books.'),
  ('hero_line2',       'Bold brands.'),
  ('hero_line3',       'Island grown.'),
  ('hero_lead',        'Guam''s locally owned accounting and social media team. Bookkeeping, payroll and content that brings customers in.'),
  ('whatsapp_number',  '16710000000'),
  ('whatsapp_display', '+1 (671) 000-0000'),
  ('email',            'pcficvaservices@gmail.com'),
  ('facebook_url',     '')
on conflict (key) do nothing;

-- 3) Services (shown on the Service Library, Accounting and Social Media pages)
create table if not exists public.services (
  id          uuid primary key default gen_random_uuid(),
  category    text not null check (category in ('accounting', 'social')),
  title       text not null,
  description text not null default '',
  icon        text not null default 'book',
  sort_order  integer not null default 0,
  created_at  timestamptz not null default now()
);

insert into public.services (category, title, description, icon, sort_order)
select * from (values
  ('accounting', 'Monthly Bookkeeping',       'Every transaction recorded, categorized and reconciled against your bank each month.', 'book',   10),
  ('accounting', 'Payroll Processing',        'Accurate, on-time payroll with pay stubs and the records you need for filings.',      'users',  20),
  ('accounting', 'Financial Statements',      'Profit & loss, balance sheet and cash flow — explained in plain language.',           'chart',  30),
  ('accounting', 'Tax-Ready Records',         'Organized books and documents so tax season is fast and stress-free for your CPA.',   'file',   40),
  ('accounting', 'Payables & Receivables',    'Bills paid on time, invoices sent and followed up so cash keeps flowing.',            'card',   50),
  ('accounting', 'Software Setup & Clean-up', 'Set up or untangle your accounting software and catch up on past months.',            'calc',   60),
  ('social',     'Content Calendar',          'A month of planned posts aligned with your promos, seasons and goals.',               'cal',    70),
  ('social',     'Graphic Design',            'On-brand posts, flyers and carousels designed to stop the scroll.',                   'pen',    80),
  ('social',     'Copywriting & Captions',    'Captions and calls-to-action written to get comments, clicks and calls.',             'file',   90),
  ('social',     'Page Management',           'Consistent posting plus replies to comments and messages on your pages.',             'social', 100),
  ('social',     'Paid Ads',                  'Targeted Facebook & Instagram ads that reach customers in Guam.',                     'target', 110),
  ('social',     'Monthly Reports',           'Reach, engagement and leads — what worked and what we''ll do next.',                  'chart',  120)
) as v(category, title, description, icon, sort_order)
where not exists (select 1 from public.services);

-- 4) Security: everyone can READ, only admins can WRITE
alter table public.settings enable row level security;
alter table public.services enable row level security;

drop policy if exists "settings read"  on public.settings;
drop policy if exists "settings write" on public.settings;
create policy "settings read"  on public.settings for select to anon, authenticated using (true);
create policy "settings write" on public.settings for all    to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "services read"  on public.services;
drop policy if exists "services write" on public.services;
create policy "services read"  on public.services for select to anon, authenticated using (true);
create policy "services write" on public.services for all    to authenticated using (public.is_admin()) with check (public.is_admin());

-- Table access (new Supabase projects do not grant this automatically; RLS above still limits writes to admins)
grant usage on schema public to anon, authenticated;
grant select on public.settings, public.services to anon, authenticated;
grant insert, update, delete on public.settings, public.services to authenticated;
grant execute on function public.is_admin() to anon, authenticated;

-- 5) Storage bucket for the logo (public images, only admins can upload/delete)
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('site', 'site', true, 5242880, array['image/png','image/jpeg','image/webp','image/svg+xml'])
on conflict (id) do nothing;

drop policy if exists "site admin select" on storage.objects;
drop policy if exists "site admin insert" on storage.objects;
drop policy if exists "site admin update" on storage.objects;
drop policy if exists "site admin delete" on storage.objects;
create policy "site admin select" on storage.objects for select to authenticated using (bucket_id = 'site' and public.is_admin());
create policy "site admin insert" on storage.objects for insert to authenticated with check (bucket_id = 'site' and public.is_admin());
create policy "site admin update" on storage.objects for update to authenticated using (bucket_id = 'site' and public.is_admin());
create policy "site admin delete" on storage.objects for delete to authenticated using (bucket_id = 'site' and public.is_admin());
