select *
from users
         left join public.posts p on users.id = p.user_id
