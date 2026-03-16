-- Staging model to clean up the raw Polars parquets
with source as (
    select *
    from {{ source('datalake', 'raw_events') }}
),

renamed as (
    select
        event_id,
        user_name,
        
        -- Explicit casting for safety
        try_cast(purchased_amt as double) as purchase_amount,
        
        cast(event_timestamp as timestamp) as event_timestamp,
        
        try_cast(event_date as date) as event_date

    from source
),

-- Best practice: Deduplicate in staging.
-- Data lakes often have duplicate files if orchestration runs multiple times.
deduped as (
    select *
    from (
        select *,
            row_number() over (partition by event_id order by event_timestamp desc) as rn
        from renamed
    )
    where rn = 1
)

select
    event_id,
    user_name,
    purchase_amount,
    event_timestamp,
    event_date
from deduped
