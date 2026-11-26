-- =====================================================================
-- PCFIC admin, part 2: CLIENTS + WhatsApp number
-- Run once in Supabase -> SQL Editor -> Run (safe to run again)
-- =====================================================================

create table if not exists public.clients (
  id              uuid primary key default gen_random_uuid(),
  slug            text not null unique,
  name            text not null,
  short_name      text not null default '',
  industry        text not null default '',
  location        text not null default '',
  about           text not null default '',
  website         text not null default '',
  services        text[] not null default '{}',
  logo_url        text not null default '',
  images          jsonb not null default '[]'::jsonb,
  show_on_clients boolean not null default true,   -- false = only in the portfolio ("other brands")
  sort_order      integer not null default 0,
  created_at      timestamptz not null default now()
);

alter table public.clients enable row level security;
drop policy if exists "clients read"  on public.clients;
drop policy if exists "clients write" on public.clients;
create policy "clients read"  on public.clients for select to anon, authenticated using (true);
create policy "clients write" on public.clients for all    to authenticated using (public.is_admin()) with check (public.is_admin());
grant select on public.clients to anon, authenticated;
grant insert, update, delete on public.clients to authenticated;

-- Current clients and portfolio brands (only added if the table is empty)
insert into public.clients (slug, name, short_name, industry, location, about, website, services, logo_url, images, show_on_clients, sort_order)
select * from (values
  ('hsp', 'Health Services of the Pacific', 'HSP', 'Healthcare', 'Dededo, Guam', 'A Guam medical clinic offering geriatric care, women''s health, diabetes care, wound care and immunizations — plus provider home visits, at-home lab draws and medical equipment for homebound patients.', '', array['Social media content','Health awareness campaigns','Graphic design','Patient-focused copywriting']::text[], 'assets/img/clients/hsp.png', '["assets/img/work/33.jpg", "assets/img/work/34.jpg", "assets/img/work/35.jpg", "assets/img/work/36.jpg", "assets/img/work/37.jpg"]'::jsonb, true, 10),
  ('career-tech-high', 'Career Tech High Academy Charter School', 'Career Tech High', 'Education', 'Guam', 'A Guam charter school focused on career and technical education — certificate courses taught on-prem, hybrid and face to face, with a proud student-athlete community.', '', array['Social media content','Event & sports graphics','Enrollment campaigns','Leadership series']::text[], 'assets/img/clients/career-tech-high-badge.png', '["assets/img/work/29.jpg", "assets/img/work/30.jpg", "assets/img/work/31.jpg", "assets/img/work/32.jpg"]'::jsonb, true, 20),
  ('upkey-aesthetics', 'Upkey Aesthetics', 'Upkey Aesthetics', 'Beauty & Aesthetics', 'Menlo Park, CA', 'An aesthetics studio offering salt facials, vitamin B12 + MIC injections, DiolazeXL laser hair removal and Ultherapy non-surgical lifting.', '', array['Social media content','Luxury brand design','Treatment carousels','Copywriting']::text[], 'assets/img/clients/upkey-aesthetics.png', '["assets/img/work/17.jpg", "assets/img/work/18.jpg", "assets/img/work/19.jpg", "assets/img/work/20.jpg"]'::jsonb, true, 30),
  ('regenerative-research', 'Regenerative Research Institute of Silicon Valley', 'Regenerative Research', 'Health & Research', 'Silicon Valley, CA', 'An institute that educates patients about regenerative medicine — cellular therapy, heart health, sports injury recovery and how the body renews itself.', 'https://regenerativeresearchsv.com', array['Educational content','Social media design','Health awareness posts']::text[], 'assets/img/clients/regenerative-research.png', '["assets/img/work/21.jpg", "assets/img/work/22.jpg", "assets/img/work/23.jpg", "assets/img/work/24.jpg"]'::jsonb, true, 40),
  ('adj-auto', 'ADJ Automotive Repair Services, LLC', 'ADJ Automotive', 'Automotive', 'Guam', 'An automotive repair shop serving drivers across Guam.', 'https://adjauto.com', array['Social media content','Graphic design']::text[], 'assets/img/clients/adj-auto.png', '[]'::jsonb, true, 50),
  ('24seven', '24Seven Gym & Sport', '24Seven Gym', 'Fitness & Sports', '', 'A gym and sports brand.', '', array['Social media content','Graphic design']::text[], 'assets/img/clients/24seven.png', '[]'::jsonb, true, 60),
  ('revival-solutions', 'Revival Solutions', 'Revival Solutions', 'Business Services', '', 'A business solutions brand.', '', array['Social media content','Graphic design']::text[], 'assets/img/clients/revival.png', '[]'::jsonb, true, 70),
  ('the-light', 'The Light A/C & Electrical Services', 'The Light', 'A/C & Electrical', '', 'Air-conditioning and electrical services.', '', array['Social media content','Graphic design']::text[], 'assets/img/clients/the-light.png', '[]'::jsonb, true, 80),
  ('lt', 'LT', 'LT', '', '', '', '', array['Social media content','Graphic design']::text[], 'assets/img/clients/lt.png', '[]'::jsonb, true, 90),
  ('guam-essential', 'Guam Essential Services', 'Guam Essential Services', '', '', '', '', '{}'::text[], '', '["assets/img/work/1.jpg", "assets/img/work/2.jpg", "assets/img/work/3.jpg", "assets/img/work/4.jpg", "assets/img/work/5.jpg"]'::jsonb, false, 100),
  ('smash-daddys', 'Smash Daddy''s', 'Smash Daddy''s', '', '', '', '', '{}'::text[], '', '["assets/img/work/6.jpg", "assets/img/work/7.jpg"]'::jsonb, false, 110),
  ('cabalen', 'Cabalen Fast Food', 'Cabalen Fast Food', '', '', '', '', '{}'::text[], '', '["assets/img/work/8.jpg", "assets/img/work/9.jpg", "assets/img/work/10.jpg", "assets/img/work/11.jpg"]'::jsonb, false, 120),
  ('bezon-buildz', 'Bezon Buildz', 'Bezon Buildz', '', '', '', '', '{}'::text[], '', '["assets/img/work/12.jpg", "assets/img/work/13.jpg", "assets/img/work/14.jpg", "assets/img/work/15.jpg", "assets/img/work/16.jpg"]'::jsonb, false, 130),
  ('wil-castro', 'Wil Castro Campaign', 'Wil Castro Campaign', '', '', '', '', '{}'::text[], '', '["assets/img/work/25.jpg", "assets/img/work/26.jpg", "assets/img/work/27.jpg", "assets/img/work/28.jpg"]'::jsonb, false, 140)
) as v(slug, name, short_name, industry, location, about, website, services, logo_url, images, show_on_clients, sort_order)
where not exists (select 1 from public.clients);

-- WhatsApp number: +1 (671) 788-8712
update public.settings set value = '16717888712',       updated_at = now() where key = 'whatsapp_number';
update public.settings set value = '+1 (671) 788-8712', updated_at = now() where key = 'whatsapp_display';
