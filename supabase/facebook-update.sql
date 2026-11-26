-- Run once in Supabase -> SQL Editor -> Run   (safe to run again)

-- 1) Facebook page link (shows the Facebook icon + "Follow us" button)
update public.settings set value = 'https://www.facebook.com/PacificVirtualAssistanceServ', updated_at = now()
where key = 'facebook_url';

-- 2) Services listed on the Facebook page that were missing on the website
update public.services set title = 'Facebook Ads Management',
       description = 'Targeted Facebook & Instagram ads that reach the right customers and bring real results.'
where title = 'Paid Ads';

insert into public.services (category, title, description, icon, sort_order)
select v.category, v.title, v.description, v.icon,
       (select coalesce(max(sort_order), 0) from public.services) + v.n
from (values
  ('social', 'Website Development',      'Fast, mobile-friendly websites that turn visitors into inquiries and bookings.', 'web',   10, 1),
  ('social', 'Professional Logo Design', 'A clean, memorable logo and brand look that makes your business stand out.',     'pen',   20, 2),
  ('social', 'Video Editing',            'Short videos and reels edited for Facebook, Instagram and TikTok.',              'video', 30, 3)
) as v(category, title, description, icon, n, k)
where not exists (select 1 from public.services s where s.title = v.title);

-- 3) Stallion work samples (the two posts), logo and services
update public.clients
set images   = '["assets/img/work/stallion-1.jpg", "assets/img/work/stallion-2.jpg"]'::jsonb,
    logo_url = 'assets/img/clients/stallion.png',
    services = array['Social media content', 'Graphic design', 'Ad creatives']::text[]
where slug = 'stallion';
