-- SQL para crear la cadena mínima de datos y usuario taquilla
-- Ejecutar en Supabase proyecto ubmalhfretticpukafgy

SET session_replication_role = 'replica';

-- 1. Operadora (tabla: admin_comercializacion_operadoras)
INSERT INTO admin_comercializacion_operadoras 
    (id, operadora, rif, direccion_id, status_id, created_at, updated_at)
SELECT 1, 'Operadora Principal', 'J-00000001-0', NULL, 1, now(), now()
WHERE NOT EXISTS (SELECT 1 FROM admin_comercializacion_operadoras WHERE id = 1);

-- 2. Bloque (tabla: admin_comercializacion_bloques)
INSERT INTO admin_comercializacion_bloques
    (id, bloque, operadora_id, status_id, created_at, updated_at)
SELECT 1, 'Bloque Principal', 1, 1, now(), now()
WHERE NOT EXISTS (SELECT 1 FROM admin_comercializacion_bloques WHERE id = 1);

-- 3. Banca (tabla: admin_comercializacion_bancas)
INSERT INTO admin_comercializacion_bancas
    (id, banca, bloque_id, status_id, created_at, updated_at)
SELECT 1, 'Banca Principal', 1, 1, now(), now()
WHERE NOT EXISTS (SELECT 1 FROM admin_comercializacion_bancas WHERE id = 1);

-- 4. Distribuidor (tabla: admin_comercializacion_distribuidores)
INSERT INTO admin_comercializacion_distribuidores
    (id, distribuidor, banca_id, status_id, created_at, updated_at)
SELECT 1, 'Distribuidor Principal', 1, 1, now(), now()
WHERE NOT EXISTS (SELECT 1 FROM admin_comercializacion_distribuidores WHERE id = 1);

-- 5. Agencia (tabla: admin_comercializacion_agencias)
INSERT INTO admin_comercializacion_agencias
    (id, agencia, distribuidor_id, status_id, created_at, updated_at)
SELECT 1, 'Agencia Principal', 1, 1, now(), now()
WHERE NOT EXISTS (SELECT 1 FROM admin_comercializacion_agencias WHERE id = 1);

-- 6. Taquilla (tabla: admin_comercializacion_taquillas)
INSERT INTO admin_comercializacion_taquillas
    (id, taquilla, agencia_id, status_id, created_at, updated_at)
SELECT 1, 'Taquilla Principal', 1, 1, now(), now()
WHERE NOT EXISTS (SELECT 1 FROM admin_comercializacion_taquillas WHERE id = 1);

SET session_replication_role = 'origin';

-- Verificacion final
SELECT 'operadoras' as tabla, COUNT(*) FROM admin_comercializacion_operadoras
UNION ALL
SELECT 'bloques', COUNT(*) FROM admin_comercializacion_bloques
UNION ALL
SELECT 'bancas', COUNT(*) FROM admin_comercializacion_bancas
UNION ALL
SELECT 'distribuidores', COUNT(*) FROM admin_comercializacion_distribuidores
UNION ALL
SELECT 'agencias', COUNT(*) FROM admin_comercializacion_agencias
UNION ALL
SELECT 'taquillas', COUNT(*) FROM admin_comercializacion_taquillas
UNION ALL
SELECT 'usuariostaquilla', COUNT(*) FROM admin_comercializacion_usuariostaquilla;
