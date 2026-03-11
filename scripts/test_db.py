import psycopg2
import socket

password = "xe5J6cSxDWj&&2U"

# The IPv6 address from nslookup
ipv6_addr = "2406:da14:271:990d:8548:e8f1:74b:8fba"

print("=== Test 1: Direct IPv6 connection ===")
try:
    conn = psycopg2.connect(
        host=ipv6_addr, port=5432, dbname="postgres",
        user="postgres", password=password,
        sslmode='require', connect_timeout=10
    )
    print("SUCCESS! IPv6 direct works!")
    cur = conn.cursor()
    cur.execute("SELECT current_database(), current_user;")
    print(f"  Result: {cur.fetchone()}")
    conn.close()
except Exception as e:
    err = str(e).strip()
    print(f"Failed: {err[:200]}")

print()
print("=== Test 2: Check IPv6 socket support ===")
try:
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((ipv6_addr, 5432))
    print("IPv6 socket connection works!")
    s.close()
except Exception as e:
    print(f"IPv6 socket failed: {e}")
    print("Your system does NOT support IPv6 connections.")

print()
print("=== Test 3: Try Google DNS to resolve IPv4 ===")
import subprocess
try:
    result = subprocess.run(['nslookup', 'db.rnmeiclskivuyzvyxmpp.supabase.co', '8.8.8.8'], 
                          capture_output=True, text=True, timeout=10)
    print(result.stdout)
except Exception as e:
    print(f"Failed: {e}")
