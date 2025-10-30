-- Create admin user and workspace for Typebot
DO $$
DECLARE
    user_id TEXT;
    workspace_id TEXT;
BEGIN
    -- Generate IDs
    user_id := 'user_' || gen_random_uuid()::text;
    workspace_id := 'workspace_' || gen_random_uuid()::text;
    
    -- Create user
    INSERT INTO "User" (id, name, email, "emailVerified", "createdAt", "updatedAt", "onboardingCategories")
    VALUES (user_id, 'Admin User', 'admin@example.com', NOW(), NOW(), NOW(), '[]'::jsonb);
    
    -- Create workspace
    INSERT INTO "Workspace" (id, name, icon, "createdAt", "updatedAt")
    VALUES (workspace_id, 'My Workspace', '🏢', NOW(), NOW());
    
    -- Link user to workspace as ADMIN
    INSERT INTO "MemberInWorkspace" (role, "userId", "workspaceId", "createdAt", "updatedAt")
    VALUES ('ADMIN', user_id, workspace_id, NOW(), NOW());
    
    RAISE NOTICE 'Created user: % and workspace: %', user_id, workspace_id;
END $$;
