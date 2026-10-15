"""Fresh post-ending paid controls; preserve failed single-coin checker."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_earned_postending_join.py').read_text().replace('audit_current_kano_earned_postending_join_runtime','audit_current_kano_postending_two_coin_join_runtime').replace('audit_current_kano_earned_postending_join_checked','audit_current_kano_postending_two_coin_join_checked')
source=source.replace("needed=['POST_ENDING_PAID_START'","needed=['POST_ENDING_ATTRACT','POST_ENDING_PAID_START'")
exec(compile(source,__file__+'::actual_attract_two_coin','exec'))
