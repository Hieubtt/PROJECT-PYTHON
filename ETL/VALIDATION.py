# 1. Check Missing
log_step(cur, "VALIDATION_MISSING", "START", "Check missing rental_id")
sql_val_missing = """
    SELECT rental_id FROM rental WHERE customer_id IS NOT NULL
    EXCEPT
    SELECT rental_id FROM warehouse_rental;
"""
missing = fetch_all(cur, sql_val_missing)
if len(missing) > 0:
    raise RuntimeError(f"Validation failed: missing {len(missing)} rental_ids.")
log_step(cur, "VALIDATION_MISSING", "SUCCESS", "No missing data")
# 2. Check Duplicates
log_step(cur, "VALIDATION_DUPLICATE", "START", "Check duplicate PK")
sql_val_dup = """
    SELECT rental_id, COUNT(*) 
    FROM warehouse_rental 
    GROUP BY rental_id HAVING COUNT(*) > 1;
"""
dup = fetch_all(cur, sql_val_dup)
if len(dup) > 0:
    raise RuntimeError(f"Validation failed: found duplicates.")
log_step(cur, "VALIDATION_DUPLICATE", "SUCCESS", "No duplicates")
print("Validation passed!")