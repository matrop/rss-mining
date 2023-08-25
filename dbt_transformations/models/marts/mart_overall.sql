{% set marts = ["mart_faz", "mart_sz", "mart_zeit"] %}

{% for mart in marts %}

select 
    article_id,
    guid,
    title,
    link,
    description,
    timestamp,
    source
from
    {{ ref(mart) }}
{% if is_incremental() %}
    where timestamp > (select max(timestamp) from {{ this }})
{% endif %}

{%- if not loop.last %}
UNION ALL
{% endif %}

{% endfor %}