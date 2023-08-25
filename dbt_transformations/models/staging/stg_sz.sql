select
    {{ dbt_utils.generate_surrogate_key(['guid']) }} :: VARCHAR as article_id,
    guid :: VARCHAR,
    title :: VARCHAR,
    link :: VARCHAR,
    description :: VARCHAR,
    timestamp :: TIMESTAMP,
    'SZ' :: VARCHAR AS source

from {{ source("raw", "sz") }}

