create table user_role
(
    id   int auto_increment
        primary key,
    user varchar(50) default '0' not null,
    role varchar(50) default '0' not null
)
    collate = utf8mb4_bin;

