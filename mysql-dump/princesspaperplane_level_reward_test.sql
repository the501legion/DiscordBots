create table level_reward_test
(
    id          int auto_increment
        primary key,
    rewardLevel int default 0 null,
    rewardRole  varchar(50)   null
)
    collate = utf8mb4_bin;

