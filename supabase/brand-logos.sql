-- Run once in Supabase -> SQL Editor -> Run
-- Adds the logos taken from the Canva portfolio and shows these brands on the Clients page.
-- (You can turn "Show on the Clients page" off again per client in the admin.)
update public.clients set logo_url = 'assets/img/clients/guam-essential.png', show_on_clients = true where slug = 'guam-essential';
update public.clients set logo_url = 'assets/img/clients/smash-daddys.png',   show_on_clients = true where slug = 'smash-daddys';
update public.clients set logo_url = 'assets/img/clients/cabalen.png',        show_on_clients = true where slug = 'cabalen';
update public.clients set logo_url = 'assets/img/clients/bezon-buildz.png',   show_on_clients = true where slug = 'bezon-buildz';
update public.clients set logo_url = 'assets/img/clients/wil-castro.png',     show_on_clients = true where slug = 'wil-castro';
