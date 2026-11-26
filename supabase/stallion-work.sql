-- Run once in Supabase -> SQL Editor -> Run  (AFTER uploading the new files to GitHub)
-- Adds the two Stallion posts as work samples, uses the logo from this site, and fills in the services.
update public.clients
set images     = '["assets/img/work/stallion-1.jpg", "assets/img/work/stallion-2.jpg"]'::jsonb,
    logo_url   = 'assets/img/clients/stallion.png',
    services   = array['Social media content', 'Graphic design', 'Ad creatives']::text[]
where slug = 'stallion';
