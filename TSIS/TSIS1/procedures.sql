CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    c_id INTEGER;
BEGIN
    SELECT id INTO c_id
    FROM contacts
    WHERE name = p_contact_name;

    IF c_id IS NULL THEN
        RAISE NOTICE 'Contact not found: %', p_contact_name;
        RETURN;
    END IF;

    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE NOTICE 'Invalid phone type: %', p_type;
        RETURN;
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (c_id, p_phone, p_type);
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    g_id INTEGER;
BEGIN
    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO g_id
    FROM groups
    WHERE name = p_group_name;

    UPDATE contacts
    SET group_id = g_id
    WHERE name = p_contact_name;

    IF NOT FOUND THEN
        RAISE NOTICE 'Contact not found: %', p_contact_name;
    END IF;
END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    out_id INTEGER,
    out_name VARCHAR,
    out_email VARCHAR,
    out_birthday DATE,
    out_group VARCHAR,
    out_phone VARCHAR,
    out_type VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.email, c.birthday, g.name, p.phone, p.type
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR g.name ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    ORDER BY c.id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION pagination(lim INT, offs INT)
RETURNS TABLE(
    out_id INTEGER,
    out_name VARCHAR,
    out_email VARCHAR,
    out_birthday DATE,
    out_group VARCHAR,
    out_date_added TIMESTAMP
)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.email, c.birthday, g.name, c.date_added
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    ORDER BY c.id
    LIMIT lim OFFSET offs;
END;
$$ LANGUAGE plpgsql;