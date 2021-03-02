create table level_banned_channel
(
    id      int auto_increment
        primary key,
    channel varchar(50) default '0' not null
)
    collate = utf8mb4_bin;

