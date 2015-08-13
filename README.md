# process-log

A utility to save the CPU and memory usage of all processes over time. This is
experimental and still in development. The idea is to be able to later go back
and check whether any processes are systematically using CPU even when inactive
(rather than checking ``top`` continuously).

To use:

    python process-log.py

Control-C to stop for now. This samples processes every 20 seconds and writes
them all to an SQLite database named ``process-log.db`` which contains the
date, process name and PID, CPU usage (in percent), as well as the real and
virtual memory in MB.

The CPU usage is the average since the last sample, so it will not miss
'spikes' in CPU - rather they will be averaged.

I will add a querying/plotting script next.
