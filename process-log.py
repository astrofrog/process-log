import os
import time
import datetime
import sqlite3

import psutil


def get_all_stats():

    values = {}
    for p in psutil.process_iter():
        try:
            cpu_percent = p.get_cpu_percent()
            memory_info = p.get_memory_info()
        except:
            pass
        else:
            values[p.pid] = {'name': p.name(),
                             'cpu': cpu_percent,
                             'rss': memory_info.rss / 1024 ** 2,
                             'vms': memory_info.vms / 1024 ** 2}

    return values

# Initial call (the psutil functions need to be called once
# before averages work)
get_all_stats()

new = not os.path.exists('pshistory.db')

conn = sqlite3.connect('pshistory.db')
c = conn.cursor()

if new:
    c.execute('CREATE TABLE history (date datetime, pid int, name text, cpu real, rss real, vms real)')

try:
    while True:
        time.sleep(20)
        now = datetime.datetime.now().isoformat()
        values = get_all_stats()

        values_to_insert = []
        for pid in values:
            d = values[pid]
            values_to_insert.append((now, pid, d['name'], d['cpu'], d['rss'], d['vms']))

        c.executemany('INSERT INTO history VALUES(?,?,?,?,?,?)', values_to_insert)

        conn.commit()

except KeyboardInterrupt:
    pass
finally:
    conn.commit()
    conn.close()
