from src.databricks_sql import DatabricksSQLClient

c = DatabricksSQLClient()
print('Client ok, http_path=', c.http_path)
try:
    c.ensure_table_exists()
    print('ensure_table_exists ok')
    rid = c.insert_plan('jane@mentee.com', 'Test plan from script', progress=5, notes='initial')
    print('inserted id', rid)
    recs = c.get_plans_by_email('jane@mentee.com')
    print('fetched', len(recs), 'records')
    if recs:
        print(recs[0]['plan'][:50])
        c.update_progress(recs[0]['id'], 20, 'updated from test')
        print('updated')
except Exception as e:
    print('ERROR', e)
