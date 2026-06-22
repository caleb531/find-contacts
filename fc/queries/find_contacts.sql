SELECT
    ZUNIQUEID,
    ZFIRSTNAME,
    ZLASTNAME,
    ZNICKNAME,
    ZORGANIZATION
FROM ZABCDRECORD
WHERE
    (
        -- First and last names are prefix matches so short Alfred searches stay
        -- fast and produce the expected "starts with" behavior
        ZFIRSTNAME LIKE :search_query_like ESCAPE '\'
        OR
        ZLASTNAME LIKE :search_query_like ESCAPE '\'
        OR
        (
            -- Match the display-style full name without requiring the Python
            -- layer to duplicate this database-specific expression
            ZFIRSTNAME IS NOT NULL
            AND
            ZLASTNAME IS NOT NULL
            AND
            (ZFIRSTNAME || ' ' || ZLASTNAME) LIKE :search_query_like ESCAPE '\'
        )
        OR
        -- Nicknames and organizations can be searched by contained words
        -- because those labels often do not begin with the typed query
        ZNICKNAME LIKE ('%' || :search_query_like) ESCAPE '\'
        OR
        ZORGANIZATION LIKE ('%' || :search_query_like) ESCAPE '\'
    )
