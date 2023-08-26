select
    {{ dbt_utils.generate_surrogate_key(['guid']) }} :: VARCHAR as article_id,
    guid :: VARCHAR,
    title :: VARCHAR,
    link :: VARCHAR,
    description :: VARCHAR,
    timestamp :: TIMESTAMP,
    'FAZ' :: VARCHAR as source 

from {{ source("raw", "faz") }}

