-- Create a session token for direct login
DO $$
DECLARE
    user_id TEXT := 'user_4f1150c7-9d97-470b-81c1-23f2fdc35ae3';
    session_id TEXT := 'session_' || gen_random_uuid()::text;
    session_token TEXT := 'dev_session_' || gen_random_uuid()::text;
BEGIN
    -- Create session
    INSERT INTO "Session" (id, "sessionToken", "userId", "expires")
    VALUES (session_id, session_token, user_id, NOW() + INTERVAL '30 days');
    
    RAISE NOTICE 'Session token: %', session_token;
END $$;
