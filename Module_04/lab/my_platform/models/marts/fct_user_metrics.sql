{{
    config(
        materialized='table'
    )
}}

with events as (
    select * from {{ ref('stg_events') }}
),

agg as (
    select
        user_name,
        count(event_id) as total_purchases,
        sum(purchase_amount) as lifetime_value,
        avg(purchase_amount) as average_order_value,
        min(event_timestamp) as first_purchase_at,
        max(event_timestamp) as last_purchase_at
    from events
    group by user_name
)

select *
from agg
