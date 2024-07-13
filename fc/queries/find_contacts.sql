SELECT
    ZUNIQUEID,
    ZFIRSTNAME,
    ZLASTNAME,
    ZNICKNAME,
    ZORGANIZATION
FROM ZABCDRECORD
WHERE
    (
        ZFIRSTNAME LIKE :search_query_like
        OR
        ZLASTNAME LIKE :search_query_like
        OR
        (
            ZFIRSTNAME IS NOT NULL
            AND
            ZLASTNAME IS NOT NULL
            AND
            (ZFIRSTNAME || ' ' || ZLASTNAME) LIKE :search_query_like
        )
        OR
        ZNICKNAME LIKE :search_query_like
        OR
        ZORGANIZATION LIKE :search_query_like
    )
    AND
    ZSYNCSTATUS = 1
