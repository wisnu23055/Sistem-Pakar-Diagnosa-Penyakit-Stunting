def calculate_cf(cf_values):
    if not cf_values:
        return 0
    
    # Validasi: Pastikan semua nilai antara 0 dan 1
    for cf in cf_values:
        if cf < 0 or cf > 1:
            raise ValueError("Nilai CF harus berada dalam rentang 0 hingga 1.")
    
    cf_combined = cf_values[0]
    for cf in cf_values[1:]:
        cf_combined = cf_combined + (cf * (1 - cf_combined))
    
    # Pastikan nilai tidak melebihi 1
    return min(cf_combined, 1)