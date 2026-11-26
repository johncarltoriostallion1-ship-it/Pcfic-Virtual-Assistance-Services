-- Run once in Supabase -> SQL Editor -> Run   (safe to run again)
-- Adds a third service group "Web & Creative" and moves the website / logo / video services into it.
alter table public.services drop constraint if exists services_category_check;
alter table public.services add constraint services_category_check
  check (category in ('accounting', 'social', 'creative'));

update public.services set category = 'creative'
where title in ('Website Development', 'Professional Logo Design', 'Video Editing');
