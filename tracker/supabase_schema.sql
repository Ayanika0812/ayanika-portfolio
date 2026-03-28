-- Run this in Supabase SQL Editor

create table if not exists visits (
  id          bigserial primary key,
  ip          text,
  country     text,
  city        text,
  region      text,
  lat         float,
  lon         float,
  device      text,
  browser     text,
  referrer    text,
  visited_at  timestamptz default now()
);

create table if not exists messages (
  id        bigserial primary key,
  name      text not null,
  email     text not null,
  message   text not null,
  sent_at   timestamptz default now()
);

-- Optional: index for faster date queries
create index on visits (visited_at desc);
create index on messages (sent_at desc);
