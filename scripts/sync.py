import os
import threading
from decimal import Decimal
from datetime import date, time, datetime
from sqlalchemy import event
from models import User, Reservation, MenuItem

# Lazy-load supabase client only when needed (not at import time)
_supabase = None
_supabase_loaded = False

def _get_supabase():
    global _supabase, _supabase_loaded
    if _supabase_loaded:
        return _supabase
    _supabase_loaded = True
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if url and key:
        try:
            from supabase import create_client
            _supabase = create_client(url, key)
            print("[OK] Supabase sync connected.")
        except Exception as e:
            print(f"[WARN] Supabase init skipped: {e}")
    return _supabase

def get_dict(obj):
    data = {}
    for c in obj.__table__.columns:
        val = getattr(obj, c.name)
        if isinstance(val, (datetime, date, time)):
            val = val.isoformat()
        elif isinstance(val, Decimal):
            val = float(val)
        data[c.name] = val
    return data

def _sync_insert(table_name, data):
    client = _get_supabase()
    if client:
        try:
            client.table(table_name).insert(data).execute()
        except Exception as e:
            print(f"Supabase sync insert error ({table_name}): {e}")

def _sync_update(table_name, data, row_id):
    client = _get_supabase()
    if client:
        try:
            client.table(table_name).update(data).eq('id', row_id).execute()
        except Exception as e:
            print(f"Supabase sync update error ({table_name}): {e}")

def _sync_delete(table_name, row_id):
    client = _get_supabase()
    if client:
        try:
            client.table(table_name).delete().eq('id', row_id).execute()
        except Exception as e:
            print(f"Supabase sync delete error ({table_name}): {e}")

def handle_insert(mapper, connection, target):
    data = get_dict(target)
    threading.Thread(target=_sync_insert, args=(target.__table__.name, data), daemon=True).start()

def handle_update(mapper, connection, target):
    data = get_dict(target)
    threading.Thread(target=_sync_update, args=(target.__table__.name, data, getattr(target, 'id', None)), daemon=True).start()

def handle_delete(mapper, connection, target):
    threading.Thread(target=_sync_delete, args=(target.__table__.name, getattr(target, 'id', None)), daemon=True).start()

def setup_supabase_sync():
    """Binds SQLAlchemy events to duplicate all Neon changes to Supabase in real-time."""
    for model in [User, Reservation, MenuItem]:
        event.listen(model, 'after_insert', handle_insert)
        event.listen(model, 'after_update', handle_update)
        event.listen(model, 'after_delete', handle_delete)
    print("[OK] Supabase sync hooks registered (lazy-load mode).")
