-- Script para eliminar usuario duplicado Aitor (aitor_marcos)
-- Transferir participaciones de aitor_marcos (ID 2) a aitor (ID 1)
UPDATE bet_participants SET user_id = 1 WHERE user_id = 2;

-- Eliminar usuario duplicado
DELETE FROM users WHERE id = 2 AND username = 'aitor_marcos';

-- Verificación
SELECT 'Usuarios restantes:' as info;
SELECT id, username, display_name FROM users ORDER BY id;

SELECT 'Participaciones de Aitor:' as info;
SELECT COUNT(*) as total FROM bet_participants WHERE user_id = 1;
