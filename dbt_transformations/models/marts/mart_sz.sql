{{
    config(
        unique_key='article_id'
    )
}}

select
    article_id,
    guid,
    title,
    link,
    description,
    category,
    timestamp,
    source

from {{ ref("stg_sz") }}

{% if is_incremental() %}
  where timestamp > (select max(timestamp) from {{ this }})
{% endif %}