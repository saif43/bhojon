from database.sync_loop import SyncLoop
from threading import Thread

def sync_loop(user_call=False):
	def get_start():
		sync_loop  = SyncLoop(user_call=user_call)

	sync_loop_thr = Thread(target=get_start, daemon=True)
	sync_loop_thr.start()
