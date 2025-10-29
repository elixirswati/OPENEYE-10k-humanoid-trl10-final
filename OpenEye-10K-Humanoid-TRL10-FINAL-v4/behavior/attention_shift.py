def next_target(dets): return ( [d for d in dets if d.get('cls')=='person'] or dets or [None])[0]
