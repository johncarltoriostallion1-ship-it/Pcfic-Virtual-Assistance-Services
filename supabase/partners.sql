-- Run once in Supabase -> SQL Editor -> Run   (safe to run again)
-- Lets any client be marked as a partner (badge on the logo, banner on their page, "Partnered with" in the footer).
alter table public.clients add column if not exists is_partner    boolean not null default false;
alter table public.clients add column if not exists partner_label text    not null default '';

-- Stallion = our website partner
update public.clients
set is_partner = true,
    partner_label = 'Official Website Partner'
where slug = 'stallion';
