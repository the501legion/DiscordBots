create table log_info
(
    id   int auto_increment
        primary key,
    text varchar(256)  null,
    time int default 0 null
)
    charset = latin1;

