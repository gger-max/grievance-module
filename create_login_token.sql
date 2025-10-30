-- Create verification token for direct login
DO $$
DECLARE
    user_email TEXT := 'admin@example.com';
    token_value TEXT := encode(gen_random_bytes(32), 'hex');
    expires_at TIMESTAMP := NOW() + INTERVAL '1 hour';
BEGIN
    -- Insert verification token
    INSERT INTO "VerificationToken" (identifier, token, expires)
    VALUES (user_email, token_value, expires_at);
    
    RAISE NOTICE 'Login URL: http://localhost:8081/api/auth/callback/email?token=%&email=%', token_value, user_email;
END $$;
