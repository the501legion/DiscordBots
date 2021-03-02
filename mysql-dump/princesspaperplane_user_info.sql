create table user_info
(
    id         varchar(50) collate utf8mb4_bin                                    null,
    name       varchar(50) collate utf8mb4_bin                                    null,
    avatar_url varchar(256) default 'https://fireabend.community/img/default.png' null,
    exp        int          default 0                                             null,
    level      int          default 0                                             null,
    expTime    int          default 0                                             null
)
    collate = latin1_general_ci;

