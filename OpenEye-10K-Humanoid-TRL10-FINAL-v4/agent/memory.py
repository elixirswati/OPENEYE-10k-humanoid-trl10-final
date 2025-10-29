import sqlite3, time, os
DB=os.environ.get('OPENEYE_MEM_DB','agent/memory.db')
SC='CREATE TABLE IF NOT EXISTS incidents(id INTEGER PRIMARY KEY,fingerprint TEXT,patch TEXT,result TEXT,created_at REAL);'

def conn():
 c=sqlite3.connect(DB); c.execute(SC); return c

def record(fp,patch,result):
 c=conn(); c.execute('INSERT INTO incidents(fingerprint,patch,result,created_at) VALUES(?,?,?,?)',(fp,patch,result,time.time())); c.commit(); c.close()

def find_patch(fp):
 c=conn(); row=c.execute("SELECT patch FROM incidents WHERE fingerprint=? AND result='success' ORDER BY id DESC LIMIT 1",(fp,)).fetchone(); c.close(); return row[0] if row else None
