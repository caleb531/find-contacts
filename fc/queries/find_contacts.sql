SELECT
    ZUNIQUEID,
    ZFIRSTNAME,
    ZLASTNAME,
    ZNICKNAME,
    ZORGANIZATION
FROM ZABCDRECORD
WHERE
    (
        ZFIRSTNAME LIKE :search_query_like ESCAPE '\'
        OR
        ZLASTNAME LIKE :search_query_like ESCAPE '\'
        OR
        (
            ZFIRSTNAME IS NOT NULL
            AND
            ZLASTNAME IS NOT NULL
            AND
            (ZFIRSTNAME || ' ' || ZLASTNAME) LIKE :search_query_like ESCAPE '\'
        )
        OR
        ZNICKNAME LIKE :search_query_like ESCAPE '\'
        OR
        ZORGANIZATION LIKE :search_query_like ESCAPE '\'
    )
    AND
    ZSYNCSTATUS = 1
